from __future__ import annotations

__all__ = ["TemporaryError"]

from typing import TYPE_CHECKING, Generic, TypeVar, Union

if TYPE_CHECKING:
    MaybeFloat = Union[int, float]

FutureT = TypeVar("FutureT")


class TemporaryError(Exception, Generic[FutureT]):
    def __init__(self, will_be_implemented_in: MaybeFloat, *, future: FutureT) -> None:
        self._implemented = will_be_implemented_in
        self._future = future

        super().__init__(
            f"Future <{self._future}> doesn't supports yet, but will be implemented in {self._implemented}."
        )
