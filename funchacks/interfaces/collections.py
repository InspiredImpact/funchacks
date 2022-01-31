from __future__ import annotations

__all__ = ["Codable", "Representable"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from types import CodeType


class Representable(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        """Overwrite of __repr__, repr(self)."""


@runtime_checkable
class Codable(Protocol):
    __code__: CodeType
