from __future__ import annotations

import inspect

import pytest

from funchacks.impl import WrapFunction
from funchacks.interfaces import Representable
from tests_tdd._tools import testlogger


@pytest.mark.usefixtures("testlogger")
def test_fn_object() -> None:
    assert issubclass(WrapFunction, Representable)

    from_func = getattr(WrapFunction, "from_function", None)
    assert from_func is not None
    assert inspect.ismethod(from_func)  # uses @classmethod

    from_func_bound = getattr(from_func, "__self__", None)
    assert from_func_bound is WrapFunction  # and bounded to FunctionWrap

    assert "flocals" in getattr(WrapFunction, "__dataclass_fields__")
