import datetime
from typing import Dict, Tuple, List

import pytest
from discord.ext.commands import Context

from discord_ext_commands_coghelper.utils import get_before_after, get_before_after_fmts
from tests import JST


@pytest.mark.parametrize(
    ("ctx", "dic", "fmt", "tzinfo", "expected"),
    [
        (
            None,  # TODO: Mock Context
            dict(before="2000-01-31", after="2000-01-01"),
            "%Y-%m-%d",
            None,
            (
                datetime.datetime(year=2000, month=1, day=31),
                datetime.datetime(year=2000, month=1, day=1),
            ),
        ),
        (
            None,  # TODO: Mock Context
            dict(),
            "%Y-%m-%d",
            None,
            (None, None),
        ),
        (
            None,  # TODO: Mock Context
            dict(before="2000-01-31", after="2000-01-01"),
            "%Y-%m-%d",
            JST,
            (
                datetime.datetime(year=2000, month=1, day=31, tzinfo=JST),
                datetime.datetime(year=2000, month=1, day=1, tzinfo=JST),
            ),
        ),
    ],
)
def test_get_before_after(
    ctx: Context,
    dic: Dict[str, str],
    fmt: str,
    tzinfo: datetime.timezone,
    expected: Tuple[datetime.datetime, datetime.datetime],
):
    assert get_before_after(ctx, dic, fmt, tzinfo) == expected


@pytest.mark.parametrize(
    ("ctx", "dic", "fmts", "tzinfo", "expected"),
    [
        (
            None,  # TODO: Mock Context
            dict(before="20000131", after="20000101"),
            ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"],
            None,
            (
                datetime.datetime(year=2000, month=1, day=31),
                datetime.datetime(year=2000, month=1, day=1),
            ),
        ),
        (
            None,  # TODO: Mock Context
            dict(before="2000#01#31", after="2000#01#01"),
            ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"],
            None,
            (None, None),
        ),
        (
            None,  # TODO: Mock Context
            dict(before="2000/01/31", after="2000/01/01"),
            ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"],
            JST,
            (
                datetime.datetime(year=2000, month=1, day=31, tzinfo=JST),
                datetime.datetime(year=2000, month=1, day=1, tzinfo=JST),
            ),
        ),
    ],
)
def test_get_before_after_fmts(
    ctx: Context,
    dic: Dict[str, str],
    fmts: List[str],
    tzinfo: datetime.timezone,
    expected: Tuple[datetime.datetime, datetime.datetime],
):
    assert get_before_after_fmts(ctx, dic, *fmts, tz=tzinfo) == expected


# TODO: test get_corrected_before_after_str
