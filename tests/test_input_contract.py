"""Regressions for metadata that previously disappeared or changed type."""
import csv
import io
from pathlib import Path

import pytest

from app.qc import analyze_records, parse_csv


def sample_records():
    return parse_csv((Path(__file__).parents[1] / 'data/stable_capable.csv').read_text())


@pytest.mark.parametrize('column', ['build_id', 'specimen_id', 'machine_id', 'notes'])
@pytest.mark.parametrize('value', [True, 42, {'batch': 'A'}, ['C1']])
def test_text_fields_reject_objects_and_numbers(column, value):
    records = sample_records()
    for row in records[:5] if column != 'specimen_id' else records[:1]:
        row[column] = value
    with pytest.raises(ValueError, match='must be text'):
        analyze_records(records)


def test_unknown_record_field_cannot_hide_mixed_machines():
    records = sample_records()
    for i, row in enumerate(records):
        del row['machine_id']
        row['machine_id '] = 'M1' if i < 5 else 'M2'
    with pytest.raises(ValueError, match='Unsupported.*machine_id'):
        analyze_records(records)


def test_unknown_csv_column_rejected_before_metadata_is_lost():
    text = (Path(__file__).parents[1] / 'data/stable_capable.csv').read_text()
    with pytest.raises(ValueError, match='Unsupported.*machine_id'):
        parse_csv(text.replace('machine_id,', 'machine_id ,', 1))


@pytest.mark.parametrize('line_ending', ['\n', '\r\n', '\r'])
def test_standard_csv_line_endings(line_ending):
    records = sample_records()
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=list(records[0]), lineterminator=line_ending)
    writer.writeheader()
    writer.writerows(records)
    result = analyze_records(parse_csv(out.getvalue()))
    assert result['metadata']['n_records'] == 200
    assert result['status'] == 'meets_target'
