from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    Context: TypeAlias = object()


def before_all(context: Context) -> None:
    context.config.setup_logging()
