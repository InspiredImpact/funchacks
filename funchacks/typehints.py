__all__ = [
    "AnyCallableT",
    "ShouldReturn",
]

from typing import Any, Callable, TypeVar

T = TypeVar("T")

AnyCallableT = TypeVar("AnyCallableT", bound=Callable[..., Any])
ShouldReturn = Callable[..., T]
