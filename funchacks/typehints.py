__all__ = [
    "AnyCallableT",
    "ShouldReturn",
    "FunctionT",
]

from types import CodeType, FunctionType
from typing import Any, Callable, Dict, Optional, Protocol, Tuple, TypeVar

T = TypeVar("T")

AnyCallableT = TypeVar("AnyCallableT", bound=Callable[..., Any])
ShouldReturn = Callable[..., T]


_T_co = TypeVar("_T_co", covariant=True)


class _FunctionLike(Protocol[_T_co]):
    __closure__: Optional[Tuple[Any, ...]]
    __code__: CodeType
    __defaults__: Optional[Tuple[Any, ...]]
    __dict__: Dict[str, Any]
    __globals__: Dict[str, Any]
    __name__: str
    __qualname__: str
    __annotations__: Dict[str, Any]
    __kwdefaults__: Dict[str, Any]


FunctionT = TypeVar(
    "FunctionT",
    FunctionType,
    _FunctionLike[Callable[..., Any]],
)
