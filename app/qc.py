"""Framework-free X-bar/R and baseline capability analysis.

Rounded constants follow NIST/SEMATECH section 6.3.2.1. Capability formulas
follow section 6.1.6, using R-bar/d2 for within-subgroup variation (C indices)
and baseline sample SD for overall performance (P indices). No specifications
are inferred from observations; no causal or predictive claims are made.
"""
from __future__ import annotations

import csv
from datetime import datetime
import io
import math
from statistics import NormalDist, mean, stdev

REQUIRED_COLUMNS = ('build_id', 'build_time', 'specimen_id', 'strength_mpa')
CONTEXT_COLUMNS = ('machine_id', 'powder_lot', 'oxygen_ppm', 'laser_power_w',
                   'scan_speed_mm_s', 'heat_treatment', 'notes')
NUMERIC_CONTEXT = {'oxygen_ppm', 'laser_power_w', 'scan_speed_mm_s'}
ALLOWED_COLUMNS = set(REQUIRED_COLUMNS + CONTEXT_COLUMNS)
# n: (A2, D3, D4, d2); published rounded constants, not fitted to uploaded data.
CONSTANTS = {
    2: (1.880, 0.000, 3.267, 1.128),
    3: (1.023, 0.000, 2.575, 1.693),
    4: (0.729, 0.000, 2.282, 2.059),
    5: (0.577, 0.000, 2.115, 2.326),
    6: (0.483, 0.000, 2.004, 2.534),
    7: (0.419, 0.076, 1.924, 2.704),
    8: (0.373, 0.136, 1.864, 2.847),
    9: (0.337, 0.184, 1.816, 2.970),
    10: (0.308, 0.223, 1.777, 3.078),
}


def _number(value, name: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or value is None or (isinstance(value, str) and not value.strip()):
        raise ValueError(f'{name} must be a finite number.')
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f'{name} must be a finite number.') from exc
    if not math.isfinite(result):
        raise ValueError(f'{name} must be a finite number.')
    if positive and result <= 0:
        raise ValueError(f'{name} must be positive.')
    return result


def parse_csv(text: str) -> list[dict]:
    """Read UTF-8 CSV text without dropping incomplete or malformed records.

    The four required headers must occur exactly once. Full numeric, ordering
    and rational-subgroup validation is performed by :func:`analyze_records`.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError('CSV is empty; supply the four required columns and observations.')
    try:
        reader = csv.DictReader(io.StringIO(text.lstrip('\ufeff'), newline=''), strict=True)
        fields = reader.fieldnames
        if not fields:
            raise ValueError('CSV needs a header row.')
        if any(not field or not field.strip() for field in fields):
            raise ValueError('CSV contains an empty header name.')
        if len(fields) != len(set(fields)):
            raise ValueError('CSV header names must be unique.')
        missing = set(REQUIRED_COLUMNS) - set(fields)
        if missing:
            raise ValueError('CSV is missing required columns: ' + ', '.join(sorted(missing)))
        unknown = set(fields) - ALLOWED_COLUMNS
        if unknown:
            raise ValueError('Unsupported CSV columns: ' + ', '.join(repr(k) for k in sorted(unknown))
                             + '. Use the exact column names in the codebook; extra fields are not silently discarded.')
        rows = []
        for row in reader:
            if None in row:
                raise ValueError(f'CSV line {reader.line_num} has more values than headers.')
            if any(value is None for value in row.values()):
                raise ValueError(f'CSV line {reader.line_num} has fewer values than headers.')
            rows.append(row)
    except csv.Error as exc:
        raise ValueError(f'Malformed CSV: {exc}') from exc
    if not rows:
        raise ValueError('CSV contains no observations.')
    return rows


def _groups_from_records(records: list[dict]) -> tuple[list[dict], int]:
    if not isinstance(records, list) or not records:
        raise ValueError('records must be a nonempty list of coupon records.')
    groups = []
    seen_builds, seen_specimens = set(), set()
    previous_time = None
    timezone_kind = None
    study_routes = {'machine_id': set(), 'heat_treatment': set()}
    for index, record in enumerate(records, 1):
        if not isinstance(record, dict):
            raise ValueError(f'Row {index} must be a record object.')
        unknown = set(record) - ALLOWED_COLUMNS
        if unknown:
            raise ValueError(f'Unsupported fields in row {index}: '
                             + ', '.join(repr(k) for k in sorted(unknown, key=str))
                             + '. Use the exact column names in the codebook.')
        for column in REQUIRED_COLUMNS:
            if column not in record or record[column] is None or str(record[column]).strip() == '':
                raise ValueError(f'Row {index} is missing {column}.')
        for column in ('build_id', 'build_time', 'specimen_id'):
            if not isinstance(record[column], str):
                raise ValueError(f'Row {index} {column} must be text.')
        build_id, specimen_id = record['build_id'].strip(), record['specimen_id'].strip()
        if specimen_id in seen_specimens:
            raise ValueError(f'Duplicate specimen_id: {specimen_id}. Each coupon is tested once.')
        seen_specimens.add(specimen_id)
        timestamp = str(record['build_time']).strip()
        try:
            if 'T' not in timestamp and ' ' not in timestamp:
                raise ValueError('timestamp requires a time')
            parsed_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError as exc:
            raise ValueError(f'Row {index}: build_time must be an ISO8601 timestamp.') from exc
        aware = parsed_time.utcoffset() is not None
        if timezone_kind is not None and aware != timezone_kind:
            raise ValueError('Use consistent timestamps: do not mix timezone-aware and naive values.')
        timezone_kind = aware
        value = _number(record['strength_mpa'], f'Row {index} strength_mpa', positive=True)
        context = {}
        for column in CONTEXT_COLUMNS:
            raw = record.get(column)
            if raw is None or (isinstance(raw, str) and not raw.strip()):
                context[column] = None
            elif column in NUMERIC_CONTEXT:
                number = _number(raw, f'Row {index} {column}')
                if number < 0:
                    raise ValueError(f'Row {index} {column} cannot be negative.')
                context[column] = number
            else:
                if not isinstance(raw, str):
                    raise ValueError(f'Row {index} {column} must be text.')
                context[column] = raw.strip()
            if column in study_routes and context[column] is not None:
                study_routes[column].add(context[column])
        if not groups or groups[-1]['id'] != build_id:
            if build_id in seen_builds:
                raise ValueError(f'Build {build_id} is not contiguous; keep each build together.')
            if previous_time is not None and parsed_time <= previous_time:
                raise ValueError('Build timestamps must be strictly increasing in input order.')
            seen_builds.add(build_id)
            previous_time = parsed_time
            groups.append({'id': build_id, 'time': timestamp, 'values': [],
                           'specimen_ids': [], 'context': context})
        else:
            if groups[-1]['time'] != timestamp:
                raise ValueError(f'Build {build_id} has inconsistent build_time values.')
            if groups[-1]['context'] != context:
                raise ValueError(f'Build {build_id} has inconsistent build metadata.')
        groups[-1]['values'].append(value)
        groups[-1]['specimen_ids'].append(specimen_id)
    sizes = {len(group['values']) for group in groups}
    if len(sizes) != 1:
        raise ValueError('All builds must have the same subgroup size; do not drop incomplete builds.')
    subgroup_size = sizes.pop()
    if subgroup_size not in CONSTANTS:
        raise ValueError('Subgroup size must be between 2 and 10 independent coupons per build.')
    for column, values in study_routes.items():
        if len(values) > 1:
            raise ValueError(f'Mixed {column} values: analyze one machine and heat-treatment route per study.')
    return groups, subgroup_size


def capability_indices(mu: float, sigma: float, lsl: float, usl: float | None,
                       prefix: str = 'C') -> dict:
    """Return unilateral or bilateral indices for a supplied positive sigma.

    C requires a within-subgroup estimator; P requires overall sample SD.
    The caller determines the appropriate population and stability warnings.
    """
    if prefix not in ('C', 'P'):
        raise ValueError('Capability prefix must be C or P.')
    if not math.isfinite(sigma) or sigma <= 0:
        raise ValueError('Variation must be positive and finite; capability is undefined.')
    lower = (mu - lsl) / (3 * sigma)
    upper = None if usl is None else (usl - mu) / (3 * sigma)
    return {prefix+'pl': lower, prefix+'pu': upper,
            prefix+'p': None if usl is None else (usl-lsl)/(6*sigma),
            prefix+'pk': None if usl is None else min(lower, upper)}


def _observed(values: list[float], lsl: float, usl: float | None) -> dict:
    below = sum(value < lsl for value in values)
    above = 0 if usl is None else sum(value > usl for value in values)
    count = len(values)
    return {'n': count, 'below_lsl': below, 'above_usl': above,
            'nonconforming': below+above,
            'fraction': (below+above)/count if count else None}


def analyze_records(records: list[dict], lsl: float = 900,
                    usl: float | None = None, baseline_builds: int = 25,
                    target: float = 1.33) -> dict:
    """Analyze ordered, equal-size rational subgroups using a frozen baseline.

    Inputs are not mutated. All returned numbers are finite (undefined indices
    are None). Baseline indices are historical estimates; chart signals suppress
    an affirmative current capability assessment. Minimum25 builds is a study
    policy for preliminary-vs-qualified interpretation, not a proof of adequacy.
    """
    lsl = _number(lsl, 'LSL', positive=True)
    usl = None if usl is None else _number(usl, 'USL', positive=True)
    target = _number(target, 'Target capability index', positive=True)
    if usl is not None and usl <= lsl:
        raise ValueError('USL must be greater than LSL.')
    if isinstance(baseline_builds, bool) or not isinstance(baseline_builds, int) or baseline_builds < 2:
        raise ValueError('baseline_builds must be an integer of at least 2.')
    groups, n = _groups_from_records(records)
    if baseline_builds > len(groups):
        raise ValueError('baseline_builds cannot exceed the number of complete builds.')
    for index, group in enumerate(groups):
        group.update(mean=mean(group['values']), range=max(group['values'])-min(group['values']),
                     phase='baseline' if index < baseline_builds else 'monitoring', signals=[])
    baseline_groups = groups[:baseline_builds]
    baseline_values = [value for group in baseline_groups for value in group['values']]
    monitoring_values = [value for group in groups[baseline_builds:] for value in group['values']]
    mu, rbar = mean(group['mean'] for group in baseline_groups), mean(group['range'] for group in baseline_groups)
    a2, d3, d4, d2 = CONSTANTS[n]
    sigma, sd = rbar / d2, stdev(baseline_values)
    if sigma <= 0 or not math.isfinite(sigma):
        raise ValueError('Baseline has zero within-build variation; control limits and capability are undefined. Check measurement resolution or collect valid data.')
    if sd <= 0 or not math.isfinite(sd):
        raise ValueError('Baseline has zero overall variation; performance indices are undefined.')
    limits = {'xbar': {'lcl': mu-a2*rbar, 'cl': mu, 'ucl': mu+a2*rbar},
              'range': {'lcl': d3*rbar, 'cl': rbar, 'ucl': d4*rbar}}
    side_previous, run_length = 0, 0
    for group in groups:
        if group['mean'] < limits['xbar']['lcl'] or group['mean'] > limits['xbar']['ucl']:
            group['signals'].append('X-bar outside 3-sigma limits')
        if group['range'] < limits['range']['lcl'] or group['range'] > limits['range']['ucl']:
            group['signals'].append('Range outside 3-sigma limits')
        side = 1 if group['mean'] > mu else (-1 if group['mean'] < mu else 0)
        run_length = run_length + 1 if side and side == side_previous else (1 if side else 0)
        if run_length >= 8:
            group['signals'].append('Eight or more consecutive means on one side')
        side_previous = side
        group['out_of_control'] = bool(group['signals'])
        group['observed'] = _observed(group['values'], lsl, usl)
    baseline_signals = sum(group['out_of_control'] for group in baseline_groups)
    monitoring_signals = sum(group['out_of_control'] for group in groups[baseline_builds:])
    capability = capability_indices(mu, sigma, lsl, usl)
    performance = capability_indices(mu, sd, lsl, usl, prefix='P')
    index_name = 'Cpl' if usl is None else 'Cpk'
    historical_index = capability[index_name]
    warnings = [
        'Capability requires representative, independent, approximately normal data and an adequate measurement system. Inspect the baseline Q-Q plot and sampling plan; no chart proves these assumptions.',
        'Coupon strength is a process proxy. This tool does not certify brackets, approve release, or establish airworthiness.',
        'Only the documented 3-sigma point and eight-on-one-side X-bar rules are applied; other special causes may go undetected.',
    ]
    if usl is None:
        warnings.append('Only a lower specification is supplied: Cpl/Ppl are used; Cp/Cpk and Pp/Ppk are undefined, not zero.')
    if any(group['context']['machine_id'] is None or group['context']['heat_treatment'] is None for group in groups):
        warnings.append('Machine or heat-treatment metadata is incomplete. Confirm one consistent production route before interpreting results.')
    if baseline_builds < 25:
        warnings.append('Fewer than 25 baseline builds: all indices are preliminary study estimates.')
    if not monitoring_values:
        warnings.append('No monitoring builds are present; this assesses the baseline only.')
    if baseline_signals:
        status = 'baseline_unstable'
        label = 'Baseline needs investigation'
        recommendation = 'Investigate baseline range and mean signals before freezing limits or interpreting capability. Retain the observations and document any justified changes to the study.'
        warnings.append('Baseline indices are descriptive historical calculations only; instability prevents a capability conclusion.')
    elif monitoring_signals:
        status = 'process_shift'
        label = 'Process signal detected'
        recommendation = 'Investigate flagged builds and their recorded conditions. The historical baseline index cannot establish current capability; review affected production under the quality procedure.'
        warnings.append('Monitoring signals are present. Do not use a good historical baseline index to endorse the changed process.')
    elif baseline_builds < 25:
        status = 'preliminary'
        label = 'More baseline evidence needed'
        recommendation = 'Collect additional representative baseline builds and review assumptions before making a capability assessment.'
    elif historical_index < target:
        status = 'below_target'
        label = 'No detected shift; margin below target'
        recommendation = 'The baseline index is below the chosen study target. Review centering and within-build variation, investigate plausible process factors, and validate any changes with a new study.'
    else:
        status = 'meets_target'
        label = 'No detected shift; baseline index meets target'
        recommendation = 'The historical baseline index meets the chosen study target, conditional on the stated assumptions. Continue monitoring and follow the separate engineering acceptance procedure.'
    result = {
        'metadata': {'n_records': len(records), 'n_builds': len(groups), 'subgroup_size': n,
                     'baseline_builds': baseline_builds, 'monitoring_builds': len(groups)-baseline_builds,
                     'lsl': lsl, 'usl': usl, 'target': target, 'units': 'MPa',
                     'index_name': index_name, 'specification': 'lower-only' if usl is None else 'two-sided',
                     'signal_rules': ['one point beyond 3-sigma X-bar or R limits', 'eight consecutive X-bar means strictly on one side'],
                     'constants': {'A2': a2, 'D3': d3, 'D4': d4, 'd2': d2}},
        'baseline': {'mean': mu, 'rbar': rbar, 'sigma_within': sigma, 'sd_overall': sd,
                     'n_builds': baseline_builds, 'n_records': len(baseline_values),
                     'capability': capability, 'performance': performance,
                     'signal_count': baseline_signals, 'index_name': index_name,
                     'index_value': historical_index, 'interpretation': 'Historical baseline estimate'},
        'limits': limits, 'groups': groups, 'status': status, 'status_label': label,
        'recommendation': recommendation, 'warnings': warnings,
        'signals': {'baseline': baseline_signals, 'monitoring': monitoring_signals,
                    'total': baseline_signals+monitoring_signals},
        'observed': {'all': _observed(baseline_values+monitoring_values, lsl, usl),
                     'baseline': _observed(baseline_values, lsl, usl),
                     'monitoring': _observed(monitoring_values, lsl, usl)},
        'qq': [{'z': NormalDist().inv_cdf((i-.5)/len(baseline_values)), 'value': value}
               for i, value in enumerate(sorted(baseline_values), 1)],
    }
    # Protect consumers from overflow caused by extreme but finite user inputs.
    def assert_finite(value):
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError('Input magnitude exceeds the numerical range; check measurement units and values.')
        if isinstance(value, dict):
            for item in value.values(): assert_finite(item)
        elif isinstance(value, list):
            for item in value: assert_finite(item)
    assert_finite(result)
    return result
