from __future__ import annotations

__all__ = ["getlocals"]

import inspect
from types import CodeType
from typing import TYPE_CHECKING, Any, Tuple, Union

from funchacks.internal import FilterGeneric, ZipGeneric


def getlocals(code: CodeType) -> ZipGeneric[Tuple[Any, Any]]:
    """Returns locals from function code object.

    Parameters:
    -----------
    code :class:`CodeType`
        Function code object.
    """
    if TYPE_CHECKING:
        varnames: Union[Tuple[str, ...], FilterGeneric[str]]

    if code.co_argcount > 0:
        spec = inspect.getargs(code)
        varnames = FilterGeneric(
            lambda v: v not in spec.args and v not in {"args", "kwargs"},
            code.co_varnames,
        )
    else:
        varnames = code.co_varnames

    return ZipGeneric(
        varnames,
        code.co_consts[1:],
    )
