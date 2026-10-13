"""Overlap-twist tests (pure interval logic, no DB needed)."""

from datetime import datetime, timedelta

SLOT = timedelta(minutes=30)


def overlaps(a_start, a_end, b_start, b_end):
    return a_start < b_end and a_end > b_start


def test_partial_overlap_rejected():
    s1 = datetime.fromisoformat("2030-01-01T10:00:00"); e1 = s1 + SLOT
    s2 = datetime.fromisoformat("2030-01-01T10:15:00"); e2 = s2 + SLOT
    assert overlaps(s1, e1, s2, e2) is True


def test_adjacent_allowed():
    s1 = datetime.fromisoformat("2030-01-01T10:00:00"); e1 = s1 + SLOT
    s2 = datetime.fromisoformat("2030-01-01T10:30:00"); e2 = s2 + SLOT
    assert overlaps(s1, e1, s2, e2) is False
