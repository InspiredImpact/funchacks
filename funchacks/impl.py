from __future__ import annotations

__all__ = ["WrapFunction", "make_wrap"]

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Tuple, TypeVar

from funchacks.inspections import getlocals
from funchacks.interfaces import Representable

if TYPE_CHECKING:
    from types import CodeType

    from funchacks.interfaces import Codable
    from funchacks.internal import ZipGeneric
    from funchacks.typehints import AnyCallableT

    _CodableT = TypeVar("_CodableT", bound=Codable)


@dataclass
class WrapFunction(Representable):
    """Class that represents function wrap object.

    Parameters:
    -----------
    code: :class:`CodeType`
        Function code object.

    flocals: :class:`ZipGeneric[Tuple[Any, Any]]` [Keyword only]
        Function locals.

    Examples:
    ---------
    >>> def foo():
    ...     a = 1
    ...
    >>> wrap = WrapFunction.from_function(foo)
    >>> wrap.flocals.asdict()
    {'a': 1}
    >>> isinstance(wrap.flocals, zip)
    True
    """

    code: CodeType
    """Function code object."""

    flocals: ZipGeneric[Tuple[Any, Any]]
    """Returns zip object that contains function locals.

    !!! Note:
        Returns not the usual :class:`zip`, but a
        modified :class:`ZipGeneric` that has the asdict() method.
    """

    def __repr__(self) -> str:
        inner = (f.name for f in getattr(self, "__dataclass_fields__").values())
        return f"{self.__class__.__name__}({', '.join(inner)})"

    @classmethod
    def from_function(cls, function: AnyCallableT, /) -> WrapFunction:
        """Returns :class:`FunctionWrap` object.

        Parameters:
        -----------
        function: :class:`AnyCallableT` [Positional only]
            Function object.
        """
        code = function.__code__
        return cls(
            code,
            flocals=getlocals(code),
        )


def make_wrap(function: _CodableT, /) -> WrapFunction:
    return WrapFunction.from_function(function)
