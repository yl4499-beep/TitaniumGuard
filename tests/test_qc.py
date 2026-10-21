import copy
import json
import math
from datetime import datetime, timedelta
from pathlib import Path

import pytest
from app.qc import analyze_records, parse_csv, capability_indices, CONSTANTS

ROOT = Path(__file__).resolve().parents[1]

def records(groups):
    result=[]
    for i, values in enumerate(groups):
        for j, value in enumerate(values):
            result.append({'build_id':f'B{i+1:03d}', 'build_time':(datetime(2026,1,1)+timedelta(days=i)).isoformat(),
                           'specimen_id':f'B{i+1}-C{j+1}', 'strength_mpa':value})
    return result

@pytest.fixture
def fixture():
    return records([[98,99,100,101,102], [99,100,101,102,103], [100,101,102,103,104]])


def test_hand_calculated_fixture_every_statistic(fixture):
    result=analyze_records(fixture, lsl=90, usl=110, baseline_builds=3)
    b=result['baseline']
    assert b['mean']==101
    assert b['rbar']==4
    assert b['sigma_within']==pytest.approx(1.7196904557179709)
    assert b['sd_overall']==pytest.approx(math.sqrt(40/14))
    assert result['limits']['xbar']==pytest.approx({'lcl':98.692,'cl':101,'ucl':103.308})
    assert result['limits']['range']==pytest.approx({'lcl':0,'cl':4,'ucl':8.46})
    assert b['capability']==pytest.approx({'Cpl':2.1321666666666665,'Cpu':1.7445,'Cp':1.9383333333333332,'Cpk':1.7445})
    assert b['performance']==pytest.approx({'Ppl':11/(3*math.sqrt(40/14)), 'Ppu':9/(3*math.sqrt(40/14)),
                                          'Pp':20/(6*math.sqrt(40/14)), 'Ppk':9/(3*math.sqrt(40/14))})
    assert result['observed']['all']=={'n':15,'below_lsl':0,'above_usl':0,'nonconforming':0,'fraction':0}
    assert result['signals']['total']==0
    assert result['status']=='preliminary'
    assert len(result['qq'])==15
    assert result['qq'][7]=={'z':0.0,'value':101.0}
    json.dumps(result, allow_nan=False)


def test_one_sided_labels_no_invented_upper(fixture):
    r=analyze_records(fixture, lsl=90, baseline_builds=3)
    assert r['metadata']['index_name']=='Cpl'
    assert r['baseline']['capability']['Cpl']==pytest.approx(2.1321666666666665)
    for name in ['Cp','Cpk','Cpu']:assert r['baseline']['capability'][name] is None
    for name in ['Pp','Ppk','Ppu']:assert r['baseline']['performance'][name] is None


def test_frozen_baseline_and_first_planted_shift(fixture):
    initial=analyze_records(fixture,lsl=90,baseline_builds=3)
    expanded=records([[98,99,100,101,102], [99,100,101,102,103], [100,101,102,103,104], [78,79,80,81,82]])
    r=analyze_records(expanded,lsl=90,baseline_builds=3)
    assert r['limits']==initial['limits']
    assert r['baseline']==initial['baseline']
    assert r['groups'][3]['signals']==['X-bar outside 3-sigma limits']
    assert r['status']=='process_shift'
    assert r['observed']['monitoring']['fraction']==1
    assert r['signals']['monitoring']==1


def test_run_eight_alert_is_not_backdated():
    baseline=[[98,99,100,101,102]]*2
    subsequent=[[99,100,101,102,103]]*9
    r=analyze_records(records(baseline+subsequent),lsl=90,baseline_builds=2)
    assert all(not group['signals'] for group in r['groups'][:9])
    assert r['groups'][9]['signals']==['Eight or more consecutive means on one side']
    assert r['groups'][10]['signals']==['Eight or more consecutive means on one side']


def test_center_hit_resets_run():
    groups=[[98,99,100,101,102]]*2+[[99,100,101,102,103]]*7+[[98,99,100,101,102]]+[[99,100,101,102,103]]*7
    r=analyze_records(records(groups),lsl=90,baseline_builds=2)
    assert r['signals']['total']==0


def test_range_signal_exists():
    r=analyze_records(records([[98,99,100,101,102]]*2+[[80,90,100,110,120]]),lsl=70,baseline_builds=2)
    assert r['groups'][-1]['signals']==['Range outside 3-sigma limits']


@pytest.mark.parametrize('n',range(2,11))
def test_supported_subgroup_sizes(n):
    data=records([list(range(100,100+n))]*3)
    r=analyze_records(data,lsl=90,baseline_builds=3)
    assert r['metadata']['subgroup_size']==n
    assert r['baseline']['sigma_within']==pytest.approx((n-1)/CONSTANTS[n][3])


@pytest.mark.parametrize('groups,match',[
    ([[100]*5,[100]*5], 'zero within-build'),
    ([[100],[101]], 'between 2 and 10'),
    ([[99,100],[99,100,101]], 'same subgroup size'),
    ([list(range(100,111))]*2,'between 2 and 10'),
])
def test_degenerate_subgroups(groups,match):
    with pytest.raises(ValueError,match=match):analyze_records(records(groups),baseline_builds=2)


@pytest.mark.parametrize('value',[None,'','NaN',float('inf'),float('-inf'),True,'x',0,-20])
def test_invalid_strength_rejected(fixture,value):
    fixture[0]['strength_mpa']=value
    with pytest.raises(ValueError):analyze_records(fixture,baseline_builds=3)


def test_missing_strength_rejected(fixture):
    del fixture[0]['strength_mpa']
    with pytest.raises(ValueError,match='missing strength_mpa'):analyze_records(fixture,baseline_builds=3)


def test_duplicates_rejected(fixture):
    fixture[1]['specimen_id']=fixture[0]['specimen_id']
    with pytest.raises(ValueError,match='Duplicate specimen_id'):analyze_records(fixture,baseline_builds=3)


def test_inconsistent_build_metadata(fixture):
    fixture[0]['oxygen_ppm']=65
    with pytest.raises(ValueError,match='inconsistent build metadata'):analyze_records(fixture,baseline_builds=3)


def test_inconsistent_build_time(fixture):
    fixture[0]['build_time']='2026-01-01T01:00:00'
    with pytest.raises(ValueError,match='inconsistent build_time'):analyze_records(fixture,baseline_builds=3)


def test_out_of_order_timestamp(fixture):
    for row in fixture[5:10]:row['build_time']='2025-12-31T00:00:00'
    with pytest.raises(ValueError,match='strictly increasing'):analyze_records(fixture,baseline_builds=3)


def test_repeated_noncontiguous_build(fixture):
    fixture.insert(5,fixture.pop(0))
    with pytest.raises(ValueError,match='not contiguous'):analyze_records(fixture,baseline_builds=3)


def test_timezone_mixing_rejected(fixture):
    for row in fixture[:5]:row['build_time']+='Z'
    with pytest.raises(ValueError,match='timezone-aware'):analyze_records(fixture,baseline_builds=3)


def test_mixed_machine_rejected(fixture):
    for i,row in enumerate(fixture):row['machine_id']='M1' if i<5 else 'M2'
    with pytest.raises(ValueError,match='Mixed machine_id'):analyze_records(fixture,baseline_builds=3)


@pytest.mark.parametrize('kwargs',[
    {'lsl':float('nan')},{'lsl':-1},{'usl':800},{'usl':900},{'target':0},
    {'baseline_builds':1},{'baseline_builds':4},{'baseline_builds':2.5},{'baseline_builds':True},
])
def test_invalid_parameters(fixture,kwargs):
    options={'baseline_builds':3};options.update(kwargs)
    with pytest.raises(ValueError):analyze_records(fixture,**options)


def test_invalid_csv_headers_and_rows():
    for text in ['', 'a,b\n1,2', 'build_id,build_time,specimen_id,strength_mpa,strength_mpa\nb,t,c,1,2',
                 'build_id,build_time,specimen_id,strength_mpa\nb,t,c',
                 'build_id,build_time,specimen_id,strength_mpa\nb,t,c,1,extra']:
        with pytest.raises(ValueError):parse_csv(text)


def test_no_input_mutation(fixture):
    before=copy.deepcopy(fixture)
    analyze_records(fixture,baseline_builds=3)
    assert fixture==before


def test_spec_boundary_is_inclusive():
    r=analyze_records(records([[90,95,100,105,110]]*3),lsl=90,usl=110,baseline_builds=3)
    assert r['observed']['all']['nonconforming']==0


def test_baseline_signal_prevents_endorsement():
    data=records([[98,99,100,101,102]]*24+[[48,49,50,51,52]])
    r=analyze_records(data,lsl=10,baseline_builds=25)
    assert r['status']=='baseline_unstable'
    assert r['baseline']['capability']['Cpl']>1.33


def test_seeded_scenarios():
    results={name:analyze_records(parse_csv((ROOT/'data'/f'{name}.csv').read_text()))
             for name in ['stable_capable','mean_shift','stable_incapable']}
    # Seed42 is an explicitly selected illustrative fixture; see data/README.md.
    for name, status in [('stable_capable', 'meets_target'), ('stable_incapable', 'below_target')]:
        assert results[name]['status']==status
        assert results[name]['signals']['total']==0
    r=results['mean_shift']
    assert r['status']=='process_shift'
    assert r['groups'][25]['id']=='B026'
    assert [g['id'] for g in r['groups'] if g['out_of_control']]==[f'B{i:03d}' for i in range(26,41)]
    assert all('X-bar outside 3-sigma limits' in g['signals'] for g in r['groups'][25:])
    assert r['limits']==results['stable_capable']['limits']
    assert r['baseline']==results['stable_capable']['baseline']
    for result in results.values():json.dumps(result,allow_nan=False)
