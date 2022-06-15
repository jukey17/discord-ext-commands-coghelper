import datetime
from typing import Union, Dict, Optional

import discord
from discord.ext.commands import Context

from discord_ext_commands_coghelper import ArgumentError
from discord_ext_commands_coghelper.utils import (
    try_strftime,
    get_datetime,
    get_datetime_fmts,
)


async def find_text_channel(
    guild: discord.Guild, message_id: int
) -> (Optional[discord.TextChannel], Optional[discord.Message]):
    """find TextChannel from Message ID

    :param guild: that has the Channel you want to find
    :type guild: Guild
    :param message_id: Message ID to look for
    :type message_id: int
    :return: TexChannel and Message instances
    :rtype: Tuple[TexChannel, Message]
    """
    for channel in guild.channels:
        if not isinstance(channel, discord.TextChannel):
            continue
        try:
            message = await channel.fetch_message(message_id)
        except (discord.NotFound, discord.Forbidden):
            pass
        except discord.HTTPException as e:
            raise e
        else:
            return channel, message
    return None


def get_before_after(
    ctx: Context, dic: Dict[str, str], fmt: str, tz: datetime.timezone = None
) -> (datetime.datetime, datetime.datetime):
    """Get a before/after value of type datetime from Dict[str, str]

    :param ctx:
    :type ctx:
    :param dic: target dict value
    :type dic: typing.Dict[str, str]
    :param fmt: for convert to datetime
    :type fmt: str
    :param tz: specify if you want an aware datetime
    :type tz: timedate.timezone
    :return: before and after datetime
    :rtype: datetime.datetime, datetime.datetime
    """
    before = get_datetime(dic, "before", fmt)
    if before and tz:
        before = before.replace(tzinfo=tz)
    after = get_datetime(dic, "after", fmt)
    if after and tz:
        after = after.replace(tzinfo=tz)

    if after is not None and before is not None and after > before:
        raise ArgumentError(ctx, before="before must be a future than after.")

    return before, after


def get_before_after_fmts(
    ctx: Context, dic: Dict[str, str], *fmts: str, tz: datetime.timezone = None
) -> (datetime.datetime, datetime.datetime):
    """Get a before/after value of type datetime from Dict[str, str]

    :param ctx:
    :type ctx:
    :param dic: target dict value
    :type dic: typing.Dict[str, str]
    :param fmts: for convert to datetime
    :type fmts: Tuple[str, ...]
    :param tz: specify if you want an aware datetime
    :type tz: timedate.timezone
    :return: before and after datetime
    :rtype: datetime.datetime, datetime.datetime
    """
    before = get_datetime_fmts(dic, "before", *fmts)
    if before and tz:
        before = before.replace(tzinfo=tz)
    after = get_datetime_fmts(dic, "after", *fmts)
    if after and tz:
        after = after.replace(tzinfo=tz)

    if after is not None and before is not None and after > before:
        raise ArgumentError(ctx, before="before must be a future than after.")

    return before, after


def get_corrected_before_after_str(
    before: datetime.datetime,
    after: datetime.datetime,
    owner: Union[discord.Guild, discord.abc.GuildChannel],
    tz: datetime.timezone,
    *fmts: str,
) -> (str, str):
    """Get a before/after datetime string considering None

    :param before: before naive datetime value
    :type before: datetime.datetime
    :param after: after naive datetime value
    :type after: datetime.datetime
    :param owner:　to use create_at when after is None
    :type owner: Union[discord.Guild, discord.abc.GuildChannel]
    :param tz: specify if you want an aware datetime
    :type tz: datetime.timezone
    :param fmts: for convert to datetime
    :type fmts: Tuple[str, ...]
    :return: before/after datetime string
    :rtype: Tuple[str, str]
    """
    if before is None:
        before = datetime.datetime.now(tz=tz)
    if after is None:
        after = owner.created_at.replace(tzinfo=datetime.timezone.utc).astimezone(tz)

    before_str = try_strftime(before, *fmts)
    after_str = try_strftime(after, *fmts)

    return before_str, after_str
