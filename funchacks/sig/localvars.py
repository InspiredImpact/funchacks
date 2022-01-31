from __future__ import annotations

__all__ = ["Bind"]

from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Generic, List, Optional, TypeVar, Union, cast

from funchacks.errors import TemporaryError

if TYPE_CHECKING:
    from funchacks.sig.impl import ArgdefSignature
    from funchacks.typehints import AnyCallableT

_T = TypeVar("_T")
VarnameT = TypeVar("VarnameT")
ValueT_co = TypeVar("ValueT_co", covariant=True)


@dataclass
class Bind(Generic[VarnameT, ValueT_co]):
    sig: ArgdefSignature
    initial: Dict[VarnameT, ValueT_co]

    @classmethod
    def from_locals(
        cls, initial: Dict[VarnameT, ValueT_co], *, in_: AnyCallableT
    ) -> Bind[VarnameT, ValueT_co]:
        sig: Optional[ArgdefSignature] = getattr(in_, "__sig__", None)
        if sig is None:
            raise AttributeError(f"Cannot find __sig__ attribute in {in_}")

        if sig.posonlycount > 0:
            raise TemporaryError(1.1, future="posonly args")

        if sig.kwonlycount > 0:
            raise TemporaryError(1.1, future="kwonly args")

        return cls(
            sig=getattr(in_, "__sig__"),
            initial=initial,
        )

    def args(self) -> List[VarnameT]:
        sig = self.sig
        return cast(
            List[VarnameT],
            sig.argnames[sig.posonlycount : (len(sig.argnames) - (len(sig.defaults) + sig.kwonlycount))],
        )

    def kwargs(self) -> List[VarnameT]:
        sig = self.sig
        return cast(
            List[VarnameT],
            sig.argnames[sig.argcount - len(sig.defaults) :],
        )

    def posonly(self) -> List[VarnameT]:
        """
        !!! Note:
            This future doesn't supports yet, but will be
            implemented in next versions.
        """
        sig = self.sig
        return cast(List[VarnameT], sig.argnames[: sig.posonlycount])

    def kwonly(self) -> List[VarnameT]:
        """
        !!! Note:
            This future doesn't supports yet, but will be
            implemented in next versions.
        """
        sig = self.sig
        return cast(
            List[VarnameT],
            sig.argnames[: -sig.kwonlycount],
        )

    def get(
        self, name: VarnameT, default: Optional[Union[ValueT_co, _T]] = None
    ) -> Optional[Union[ValueT_co, _T]]:
        return self.initial.get(name, default)
