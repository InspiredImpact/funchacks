from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    ContextT = TypeVar("ContextT")


def before_all(context: ContextT) -> None:
    context.config.setup_logging()
