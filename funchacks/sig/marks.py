__all__ = ["Argument", "arg", "kwarg", "posonly", "kwonly"]

import inspect
from dataclasses import dataclass
from typing import Any

from typing_extensions import TypeAlias

from funchacks.internal import MISSING

_TYPE: TypeAlias = object


@dataclass
class Argument:
    """Dataclass that represents function Argument.

    Parameters:
    -----------
    name: :class:`str`
        Argument name.

    type: :class:`Literal[0, 1]`
        Type of the argument (default or posonly).

        !!! Note:
            *args, **kwargs and kwonly args are currently not
            supported due to the fact that the way I chose to
            change the function signature is very unclean and
            every time there are a lot of bugs, maybe in future
            versions it will be added.

    default: :class:`Any` = MISSING
        Default value of keyword argument.

        !!! Note:
            Positional only arguments cannot have a default
            value, otherwise an error will be raised.
    """

    name: str
    type: _TYPE
    default: Any = MISSING

    def __post_init__(self) -> None:
        if self.type is inspect.Parameter.POSITIONAL_ONLY and self.default is not MISSING:
            raise ValueError("Positional only arguments cannot have a default value.")


def arg(name: str) -> Argument:
    """Wrap that represents default function argument.

    Parameters:
    -----------
    name: :class:`str`
        Default parameter name.
    """
    return Argument(name, inspect.Parameter.POSITIONAL_OR_KEYWORD)


def kwarg(name: str, value: Any = MISSING) -> Argument:
    """Wrap that represents keyword function argument.

    Parameters:
    -----------
    name: :class:`str`
        Keyword parameter name.

    value: :class:`Any` = MISSING
        Argument default value.
    """
    return Argument(name, inspect.Parameter.POSITIONAL_OR_KEYWORD, value)


def posonly(name: str) -> Argument:
    """Wrap that represents positional only function argument.

    !!! Note:
        This future doesn't supports yet, but will be
        implemented in next versions.

    Parameters:
    -----------
    name: :class:`str`
        Positional only parameter name.
    """
    return Argument(name, inspect.Parameter.POSITIONAL_ONLY)


def kwonly(name: str, value: Any = MISSING) -> Argument:
    """Wrap that represents keywordonly function argument.

    !!! Note:
        This future doesn't supports yet, but will be
        implemented in next versions.

    Parameters:
    -----------
    name: :class:`str`
        Keywordonly parameter name.

    value: :class:`Any` = MISSING
        Argument default value.
    """
    return Argument(name, inspect.Parameter.KEYWORD_ONLY, value)
