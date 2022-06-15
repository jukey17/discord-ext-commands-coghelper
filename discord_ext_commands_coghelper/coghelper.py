import logging
import re
from typing import Dict, Tuple, Any

from discord import Embed
from discord.ext.commands import Bot
from discord.ext.commands.context import Context

from discord_ext_commands_coghelper import ArgumentError, ExecutionError

logger = logging.getLogger(__name__)


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


class CogHelper:
    """Base class to assist classes using discord.ext.commands.Cog features"""

    def __init__(self, bot: Bot):
        """__init__

        :param bot: Bot instance
        :type bot: discord.ext.commands.Bot
        """
        self._bot = bot

    @property
    def bot(self) -> Bot:
        """BOT instances that use yourself

        :rtype: discord.ext.commands.Bot
        """
        return self._bot

    async def execute(self, ctx: Context, args: Tuple[Any]):
        """Execute command

        You can use the functionality of this class by calling this method from the command method of the inherited
        class

        :param ctx: context from discord.py command
        :type ctx: discord.ext.commands.context.Context
        :param args: arguments from discord.py command
        :type args: Tuple[Any]
        :return: None
        :rtype: None
        """
        logger.debug(
            f"{ctx.command} executor={ctx.author}, guild={ctx.guild}, channel={ctx.channel}, args={args}"
        )

        if ctx.author.bot:
            if not self._on_execute_by_bot():
                return

        async with ctx.typing():
            try:
                self._parse_args(ctx, _parse_tuple_args(args))
            except ArgumentError as e:
                await self._send_argument_error(ctx, e)
                return

            try:
                await self._execute(ctx)
            except ExecutionError as e:
                await self._send_execution_error(ctx, e)

    def _on_execute_by_bot(self) -> bool:
        """Called by BOT on execute command

        This function can be defined in an inherited class to change its behavior

        :return:If True is returned, processing continues
        :rtype: bool
        """
        logger.warning("this is bot, not execute command.")
        return False

    def _parse_args(self, ctx: Context, args: Dict[str, str]):
        """Parse arguments

        By defining this method in the inherited class, arguments formatted as Dict[str, str] types can be parsed.

        :param ctx: context in which the command was executed
        :type ctx: discord.ext.commands.context.Context
        :param args: arguments
        :type args: Dict[str, str]
        :return: None
        :rtype: None
        """
        return NotImplementedError("this method is must be override.")

    async def _execute(self, ctx: Context):
        """Execute command

        Define this method in a class that extends it for actual command processing

        :param ctx: context in which the command was executed
        :type ctx: discord.ext.commands.context.Context
        :return: None
        :rtype: None
        """
        return NotImplementedError("this method is must be override.")

    async def _send_argument_error(self, ctx: Context, error: ArgumentError) -> None:
        logger.warning(f"send ArgumentError={error}")
        title = error.title
        description = (
            error.description if not error.description else ctx.message.content
        )
        embed = Embed(title=title, description=description)
        for key, value in error.causes.items():
            embed.add_field(name=key, value=value)
        await ctx.send(embed=embed)

    async def _send_execution_error(self, ctx: Context, error: ExecutionError) -> None:
        logger.warning(f"send ExecutionError={error}")
        description = (
            error.description if not error.description else ctx.message.content
        )
        embed = Embed(title=error.title, description=description)
        for key, value in error.causes.items():
            embed.add_field(name=key, value=value)
        await ctx.send(embed=embed)
