import datetime
from typing import List

import pytest

from discord_ext_commands_coghelper.utils import (
    to_utc_naive,
    try_strptime,
    try_strftime,
)
from tests import JST, UTC


@pytest.mark.parametrize(
    ("dt", "expected"),
    [
        (
            datetime.datetime(2000, 1, 1, 9, 0, 0, 0, JST),
            datetime.datetime(2000, 1, 1, 0, 0, 0, 0),
        ),
        (
            datetime.datetime(2000, 1, 1, 0, 0, 0, 0, UTC),
            datetime.datetime(2000, 1, 1, 0, 0, 0, 0),
        ),
        (None, None),
    ],
)
def test_to_utc_naive(dt: datetime.datetime, expected):
    assert to_utc_naive(dt) == expected


@pytest.mark.parametrize(
    ("data", "fmts", "default", "expected"),
    [
        (
            "2000-01-01",
            ["%Y%m%d", "%Y-%m-%d", "%Y/%m/%d"],
            None,
            datetime.datetime(year=2000, month=1, day=1),
        ),
        (
            "20000101",
            ["%Y/%m/%d"],
            None,
            None,
        ),
    ],
)
def test_try_strptime(data: str, fmts: List[str], default: datetime.datetime, expected):
    assert try_strptime(data, *fmts, default=default) == expected


@pytest.mark.parametrize(
    ("dt", "fmts", "default", "expected"),
    [
        (
            datetime.datetime(year=2000, month=1, day=1),
            ["%Y%m%d", "%Y-%m-%d", "%Y/%m/%d"],
            None,
            "20000101",
        ),
        (
            datetime.datetime(year=2000, month=1, day=1),
            ["invalid"],
            "invalid",
            "invalid",
        ),
    ],
)
def test_try_strftime(dt: datetime.datetime, fmts: List[str], default: str, expected):
    assert try_strftime(dt, *fmts, default=default) == expected
