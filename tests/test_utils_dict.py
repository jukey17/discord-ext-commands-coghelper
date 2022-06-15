import datetime
from typing import Dict, Callable, List, Any

import pytest

from discord_ext_commands_coghelper.utils import (
    get_bool,
    get_list,
    get_datetime,
    get_datetime_fmts,
)


@pytest.mark.parametrize(
    ("dic", "key", "default", "expected"),
    [
        (dict(key="False"), "key", True, False),
        (dict(key="false"), "key", True, False),
        (dict(key="FALSE"), "key", True, False),
        (dict(key="True"), "key", False, True),
        (dict(key="true"), "key", False, True),
        (dict(key="TRUE"), "key", False, True),
        (dict(key="False"), "does_not_exist_key", True, True),
        (dict(key="True"), "does_not_exist_key", False, False),
    ],
)
def test_get_bool(dic: Dict[str, str], key: str, default: bool, expected: bool):
    assert get_bool(dic, key, default) == expected


@pytest.mark.parametrize(
    ("dic", "key", "delimiter", "predicate", "default", "expected"),
    [
        (dict(key="a,b,c"), "key", ",", None, [], ["a", "b", "c"]),
        (dict(key="1,2,3"), "key", ",", lambda v: int(v), [], [1, 2, 3]),
        (dict(key="a,b,c"), "does_not_exist_key", ",", None, [], []),
    ],
)
def test_get_list(
    dic: Dict[str, str],
    key: str,
    delimiter: str,
    predicate: Callable[[str], Any],
    default: List[Any],
    expected: Any,
):
    assert get_list(dic, key, delimiter, predicate, default) == expected


@pytest.mark.parametrize(
    ("dic", "key", "fmt", "default", "expected"),
    [
        (
            dict(key="2000-01-01"),
            "key",
            "%Y-%m-%d",
            None,
            datetime.datetime(year=2000, month=1, day=1),
        ),
        (
            dict(key="2000/01/01 20:30:59"),
            "key",
            "%Y/%m/%d %H:%M:%S",
            None,
            datetime.datetime(year=2000, month=1, day=1, hour=20, minute=30, second=59),
        ),
        (
            dict(key="2000-01-01"),
            "does_not_exist_key",
            "%Y-%m-%d",
            datetime.datetime(year=2000, month=1, day=1),
            datetime.datetime(year=2000, month=1, day=1),
        ),
    ],
)
def test_get_datetime(
    dic: Dict[str, str],
    key: str,
    fmt: str,
    default: datetime.datetime,
    expected: datetime.datetime,
):
    assert get_datetime(dic, key, fmt, default) == expected


@pytest.mark.parametrize(
    ("dic", "key", "fmts", "default", "expected"),
    [
        (
            dict(key="20000101"),
            "key",
            ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"],
            None,
            datetime.datetime(year=2000, month=1, day=1),
        ),
        (
            dict(key="1990/06/30"),
            "key",
            ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"],
            None,
            datetime.datetime(year=1990, month=6, day=30),
        ),
        (
            dict(key="2000-01-01"),
            "does_not_exist_key",
            ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"],
            datetime.datetime(year=2000, month=1, day=1),
            datetime.datetime(year=2000, month=1, day=1),
        ),
    ],
)
def test_get_datetime_fmts(
    dic: Dict[str, str],
    key: str,
    fmts: List[str],
    default: datetime.datetime,
    expected: datetime.datetime,
):
    assert get_datetime_fmts(dic, key, *fmts, default=default) == expected
