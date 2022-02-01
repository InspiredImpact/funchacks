from __future__ import annotations

__all__ = ["Representable"]

from abc import ABC, abstractmethod


class Representable(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        """Overwrite of __repr__, repr(self)."""
