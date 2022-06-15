import datetime
from typing import Optional


def to_utc_naive(dt: datetime.datetime) -> Optional[datetime.datetime]:
    """Convert to utc naive datetime

    :param dt: aware datetime
    :type dt: datetime.datetime
    :return: utc naive datetime
    :rtype: datetime.datetime
    """
    if dt is None:
        return None
    return dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)


def try_strptime(
    data: str, *fmts: str, default: datetime.datetime = None
) -> datetime.datetime:
    """Try using multiple formats for datetime.datetime.strptime

    :param data: data string
    :type data: str
    :param fmts: for convert to datetime
    :type fmts: Tuple[str, ...]
    :param default: default value if cannot be parsed
    :type default: datetime.datetime
    :return: parsed datetime value
    :rtype: datetime.datetime
    """
    for fmt in fmts:
        # noinspection PyBroadException
        try:
            dt = datetime.datetime.strptime(data, fmt)
        except Exception:
            continue
        else:
            return dt
    return default


def try_strftime(dt: datetime.datetime, *fmts: str, default: str = None) -> str:
    """Try using multiple formats for datetime.datetime.strftime

    :param dt: datetime value
    :type dt: datetime.datetime
    :param fmts: for convert to str
    :type fmts: Tuple[str, ...]
    :param default: default value if cannot be formatted
    :type default: str
    :return: formmated string value
    :rtype: str
    """
    for fmt in fmts:
        # noinspection PyBroadException
        try:
            value = dt.strftime(fmt)
        except Exception:
            continue
        else:
            return value
    return default
