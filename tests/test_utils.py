import pytest

from discord_ext_commands_coghelper import *

JST = datetime.timezone(datetime.timedelta(hours=9), "JST")
UTC = datetime.timezone.utc


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
    assert get_before_after_fmts(ctx, dic, *fmts, tzinfo=tzinfo) == expected
