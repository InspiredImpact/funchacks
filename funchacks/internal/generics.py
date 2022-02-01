__all__ = ["ZipGeneric", "FilterGeneric"]

from typing import TYPE_CHECKING, Generic, Iterator, TypeVar

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


class ZipGeneric(zip, Generic[T_co]):  # type: ignore
    """Making :class:`zip` as generic in <py3.9"""

    if TYPE_CHECKING:

        def __iter__(self) -> Iterator[T_co]:
            ...

        def __next__(self) -> T_co:
            ...


class FilterGeneric(filter, Generic[T]):  # type: ignore
    """Making :class:`filter` as generic in <py3.9"""

    if TYPE_CHECKING:

        def __iter__(self) -> Iterator[T]:
            ...
