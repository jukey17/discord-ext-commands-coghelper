from typing import Dict, Optional, Any

from discord import ChannelType
from discord.abc import GuildChannel
from discord.ext.commands import Context


class _ErrorBase(Exception):
    def __init__(self, title: str, description: str, causes: Dict[str, Any]):
        self._title = title if title.startswith("⚠️") else f"⚠️{title}"
        self._description = description
        self._causes = causes

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def causes(self) -> Dict[str, Any]:
        return self._causes

    def __str__(self):
        causes = ", ".join([f"{key}={value}" for key, value in self.causes.items()])
        return f"[title={self.title}, description={self.description}, {causes}]"


class ArgumentError(_ErrorBase):
    """Used when there is a problem with the argument

    Please raise in the _parse_args function
    """

    def __init__(self, ctx: Context, **kwargs):
        super().__init__(
            kwargs.pop("title", "Argument Error"),
            kwargs.pop("description", ctx.message.content),
            kwargs,
        )


class ExecutionError(_ErrorBase):
    """Used when there is a problem with Execute method

    Please raise in the _execute function
    """

    def __init__(self, ctx: Context, **kwargs):
        super().__init__(
            kwargs.pop("title", "Execution Error"),
            kwargs.pop("description", ctx.message.content),
            kwargs,
        )


class ChannelNotFoundError(ExecutionError):
    """Used when a channel could not be found

    Please raise in the _execute function
    """

    def __init__(self, ctx: Context, channel_id, **kwargs):
        super().__init__(ctx, title="Channel NotFound", channel_id=channel_id, **kwargs)


class ChannelTypeError(ExecutionError):
    """Used when a channel type is wrong

    Please raise in the _execute function
    """

    def __init__(self, ctx: Context, channel: GuildChannel, required_type: ChannelType):
        super().__init__(
            ctx,
            title="ChannelType is incorrect",
            channel=channel.mention,
            required=str(required_type),
        )


class UserNotFoundError(ExecutionError):
    """Used when a user could not be found

    Please raise in the _execute function
    """

    def __init__(self, ctx: Context, user_id, **kwargs):
        super().__init__(ctx, title="User NotFound", user_id=user_id, **kwargs)
