"""Integration checks for public API behavior, independent of UI rendering."""
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.server import api

client=TestClient(api)

def test_health():
    r=client.get('/health'); assert r.status_code==200 and r.json()['status']=='ok'

@pytest.mark.parametrize('name,status',[('stable_capable','meets_target'),('mean_shift','process_shift'),('stable_incapable','below_target')])
def test_dataset_roundtrip(name,status):
    csv=client.get('/api/datasets/'+name);assert csv.status_code==200
    r=client.post('/api/analyze',json={'csv_text':csv.text});assert r.status_code==200
    a=r.json();assert a['status']==status and a['metadata']['n_records']==200
    assert a['baseline']['capability']['Cpk'] is None

def test_invalid_csv_is_actionable():
    r=client.post('/api/analyze',json={'csv_text':'a,b\n1,2'});assert r.status_code==422
    assert 'missing required columns' in r.json()['detail']

def test_mutually_exclusive_inputs():
    r=client.post('/api/analyze',json={'csv_text':'x','records':[]});assert r.status_code==422
    assert 'exactly one' in r.json()['detail']

def test_unknown_dataset():assert client.get('/api/datasets/not-a-file').status_code==404

def test_noninteger_baseline_rejected():
    r=client.post('/api/analyze',json={'records':[],'baseline_builds':2.5});assert r.status_code==422

def test_metadata_is_synthetic():
    r=client.get('/api/datasets');assert len(r.json())==3 and all(x['synthetic'] for x in r.json())

@pytest.fixture
def valid_csv():
    return client.get('/api/datasets/stable_capable').text


@pytest.mark.parametrize('field,value',[
    ('lsl',True), ('target',True), ('usl',True),
    ('lsl','900'), ('target','1.33'), ('usl','1100'),
])
def test_specs_are_strict_numbers(valid_csv,field,value):
    payload={'csv_text':valid_csv,'lsl':0.5,field:value}
    r=client.post('/api/analyze',json=payload)
    assert r.status_code==422
    assert any(error['loc'][-1]==field for error in r.json()['detail'])


def test_unknown_field_is_not_silently_ignored(valid_csv):
    r=client.post('/api/analyze',json={'csv_text':valid_csv,'targte':10})
    assert r.status_code==422
    assert r.json()['detail'][0]['loc']==['body','targte']
    assert r.json()['detail'][0]['type']=='extra_forbidden'


@pytest.mark.parametrize('field,value',[
    ('baseline_builds','NaN'), ('baseline_builds','Infinity'),
    ('csv_text','NaN'), ('csv_text','Infinity'),
    ('lsl','NaN'), ('lsl','Infinity'), ('lsl','-Infinity'),
    ('target','NaN'), ('usl','Infinity'),
])
def test_nonfinite_raw_json_returns_safe_actionable_422(field,value):
    # JSON parsers may accept these nonstandard literals; never reflect them
    # into a JSON response where NaN/Infinity would raise another exception.
    safe_client=TestClient(api,raise_server_exceptions=False)
    raw='{"records":[],"'+field+'":'+value+'}'
    r=safe_client.post('/api/analyze',content=raw,headers={'Content-Type':'application/json'})
    assert r.status_code==422
    errors=r.json()['detail']
    assert isinstance(errors,list) and errors
    assert any(error['loc'][-1]==field for error in errors)
    assert all(set(error)=={'loc','msg','type'} for error in errors)


@pytest.mark.parametrize('field', ['lsl','target','usl'])
@pytest.mark.parametrize('value', [0,-1])
def test_specs_must_be_positive(valid_csv,field,value):
    r=client.post('/api/analyze',json={'csv_text':valid_csv,field:value})
    assert r.status_code==422
    assert any(error['loc'][-1]==field for error in r.json()['detail'])


def test_integer_numeric_specs_remain_accepted(valid_csv):
    r=client.post('/api/analyze',json={'csv_text':valid_csv,'lsl':900,'usl':1100,'target':2,'baseline_builds':25})
    assert r.status_code==200
    assert r.json()['metadata']['lsl']==900
    assert r.json()['metadata']['usl']==1100
    assert r.json()['metadata']['target']==2


def test_record_count_rejected_before_analysis():
    r=client.post('/api/analyze',json={'records':[{}]*20_001})
    assert r.status_code==422
    assert r.json()['detail'][0]['loc']==['body','records']
    assert r.json()['detail'][0]['type']=='too_long'


def test_missing_source_is_actionable():
    r=client.post('/api/analyze',json={})
    assert r.status_code==422
    assert 'exactly one' in r.json()['detail']


def test_malformed_json_is_actionable_and_safe():
    r=client.post('/api/analyze',content='{"records":',headers={'Content-Type':'application/json'})
    assert r.status_code==422
    errors=r.json()['detail']
    assert errors[0]['type']=='json_invalid'
    assert all(set(error)=={'loc','msg','type'} for error in errors)


def test_known_answer_api_fixture():
    records=[]
    for i,values in enumerate([[98,99,100,101,102],[99,100,101,102,103],[100,101,102,103,104]],1):
        for j,value in enumerate(values,1):
            records.append({'build_id':f'B{i}','build_time':f'2026-01-0{i}T08:00:00',
                            'specimen_id':f'B{i}-C{j}','strength_mpa':value})
    r=client.post('/api/analyze',json={'records':records,'lsl':90,'usl':110,'baseline_builds':3})
    assert r.status_code==200
    result=r.json()
    assert result['baseline']['mean']==101
    assert result['baseline']['capability']['Cpk']==pytest.approx(1.7445)
    assert result['limits']['xbar']==pytest.approx({'lcl':98.692,'cl':101,'ucl':103.308})

@pytest.mark.parametrize('prefix',['','/content/titanium'])
def test_docs_use_local_assets_and_correct_root_path(prefix):
    from fastapi import FastAPI
    if prefix:
        host=FastAPI()
        host.mount(prefix,api)
        docs_client=TestClient(host)
    else:
        docs_client=client
    r=docs_client.get(prefix+'/docs')
    assert r.status_code==200
    assert f'src="{prefix}/assets/vendor/swagger-ui-bundle.js"' in r.text
    assert f'href="{prefix}/assets/vendor/swagger-ui.css"' in r.text
    assert f"url: '{prefix}/openapi.json'" in r.text
    assert 'cdn.jsdelivr.net' not in r.text
    assert 'fastapi.tiangolo.com/img/favicon.png' not in r.text
    assert 'data:image/svg+xml' in r.text
    for name,content_type,marker in [('swagger-ui-bundle.js','javascript','SwaggerUIBundle'),('swagger-ui.css','text/css','.swagger-ui')]:
        asset=docs_client.get(prefix+'/assets/vendor/'+name)
        assert asset.status_code==200
        assert content_type in asset.headers['content-type']
        assert marker in asset.text
    assert docs_client.get(prefix+'/openapi.json').status_code==200
    assert docs_client.get(prefix+'/redoc').status_code==404
