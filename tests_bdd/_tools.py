from __future__ import annotations

__all__ = ["has_args", "function_template"]

from typing import TYPE_CHECKING, Any, Generator, Generic, Optional, TypeVar

from behave import fixture
from hamcrest.core.base_matcher import BaseMatcher

if TYPE_CHECKING:
    from hamcrest.core.description import Description

    from funchacks.typehints import AnyCallableT

    ContextT = TypeVar("ContextT")

ItemT = TypeVar("ItemT")


class HasAttributes(BaseMatcher, Generic[ItemT]):
    def __init__(self, *attrs: str) -> None:
        self.attrs = attrs
        self.failed: Optional[str] = None

    def _matches(self, item: ItemT) -> bool:
        for attr in self.attrs:
            if not hasattr(item, attr):
                self.failed = attr
                return False
        return True

    def describe_to(self, description: Description) -> None:
        (description.append_text("failing on ").append_text(f"<{self.failed}> attribute"))


def has_args(*attributes: str) -> HasAttributes[ItemT]:
    return HasAttributes(*attributes)


@fixture
def function_template(_: ContextT) -> Generator[AnyCallableT, Any, None]:
    """Fixture that returns function object (template for many steps)."""

    def foo(a: int, /, b: int, *, c: int) -> None:
        # Some random code for testing locals and sig args.
        d = 1
        e = 2
        return None

    yield foo
