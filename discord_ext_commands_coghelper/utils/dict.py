import datetime
from typing import Dict, Callable, List, Any

from discord_ext_commands_coghelper.utils import try_strptime


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


def get_datetime_fmts(
    dic: Dict[str, str], key: str, *fmts: str, default: datetime.datetime = None
) -> datetime.datetime:
    """Get a value of type datetime from Dict[str, str]

    :param dic: target dict value
    :type dic: typing.Dict[str, str]
    :param key: key to get the value
    :type key: str
    :param fmts: for convert to datetime
    :type fmts: Tuple[str, ...]
    :param default: default value if key does not exist
    :type default: datetime.datetime
    :return: datetime value
    :rtype: datetime.datetime
    """
    if key not in dic:
        return default
    return try_strptime(dic[key], *fmts, default=default)
