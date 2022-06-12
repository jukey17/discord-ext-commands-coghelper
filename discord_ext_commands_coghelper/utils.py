import datetime
import re
from typing import Dict, Callable, Any, List, Tuple

from discord.ext.commands import Context

from discord_ext_commands_coghelper import ArgumentError


def get_bool(dic: Dict[str, str], key: str, default: bool = False) -> bool:
    """Get a value of type bool from Dict[str, str]

    :param dic: target dict value
    :type dic: typing.Dict[str, str]
    :param key: key to get the value
    :type key: str
    :param default: default value if key does not exist
    :type default: bool
    :return: bool value
    :rtype: bool
    """
    if key not in dic:
        return default
    return True if dic[key].lower() != "false" else False


def get_list(
    dic: Dict[str, str],
    key: str,
    delimiter: str,
    predicate: Callable[[str], Any] = None,
    default: List[Any] = None,
) -> List[Any]:
    """Get a value of type List from Dict[str, str]

    :param dic: target dict value
    :type dic: typing.Dict[str, str]
    :param key: key to get the value
    :type key: str
    :param delimiter: for splitting to multiple elements
    :type delimiter: str
    :param predicate: for processing the string after splitting
    :type predicate: typing.Callable[[str], Any]
    :param default: default value if key does not exist
    :type default: List[Any]
    :return: list value
    :rtype: List[Any]
    """
    if key not in dic:
        return default
    if not predicate:
        return [value for value in dic[key].split(delimiter)]
    return [predicate(value) for value in dic[key].split(delimiter)]


def get_datetime(
    dic: Dict[str, str], key: str, fmt: str, default: datetime.datetime = None
) -> datetime.datetime:
    """Get a value of type datetime from Dict[str, str]

    :param dic: target dict value
    :type dic: typing.Dict[str, str]
    :param key: key to get the value
    :type key: str
    :param fmt: for convert to datetime
    :type fmt: str
    :param default: default value if key does not exist
    :type default: datetime.datetime
    :return: datetime value
    :rtype: datetime.datetime
    """
    if key not in dic:
        return default
    return datetime.datetime.strptime(dic[key], fmt)


def get_before_after(
    ctx: Context, dic: Dict[str, str], fmt: str, tzinfo: datetime.timezone = None
) -> (datetime.datetime, datetime.datetime):
    """Get a before/after value of type datetime from Dict[str, str]

    :param ctx:
    :type ctx:
    :param dic: target dict value
    :type dic: typing.Dict[str, str]
    :param fmt: for convert to datetime
    :type fmt: str
    :param tzinfo: specify if you want an aware datetime
    :type tzinfo: timedate.timezone
    :return: before and after datetime
    :rtype: datetime.datetime, datetime.datetime
    """
    before = get_datetime(dic, "before", fmt)
    if before and tzinfo:
        before = before.replace(tzinfo=tzinfo)
    after = get_datetime(dic, "after", fmt)
    if after and tzinfo:
        after = after.replace(tzinfo=tzinfo)

    if after is not None and before is not None and after > before:
        raise ArgumentError(ctx, before="before must be a future than after.")

    return before, after


def _parse_tuple_args(args: Tuple[Any]) -> Dict[str, str]:
    parsed: Dict[str, str] = {}
    for arg in args:
        if not isinstance(arg, str):
            continue
        result = re.match(r"(.*)=(.*)", arg)
        if result is None:
            parsed[arg] = "True"
        else:
            parsed[result.group(1)] = result.group(2)

    return parsed
