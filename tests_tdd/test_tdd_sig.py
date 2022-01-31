import inspect
from dataclasses import is_dataclass

import pytest

from funchacks import sig
from tests_tdd._tools import has_args, testlogger


@pytest.mark.usefixtures("testlogger")
def test_sig() -> None:
    assert has_args(
        sig,
        "change_args",
        "from_function",
        "Argument",
        "arg",
        "kwarg",
        "posonly",
    )


@pytest.mark.usefixtures("testlogger")
def test_sig_argument_base() -> None:
    assert is_dataclass(sig.Argument)

    kwarg = sig.Argument(
        name="some_arg",
        default=None,
        type=inspect.Parameter.POSITIONAL_OR_KEYWORD,
    )
    assert has_args(kwarg, "name", "default", "type")

    assert isinstance(sig.arg("arg"), sig.Argument)
    assert isinstance(sig.kwarg("kwarg", None), sig.Argument)
    assert isinstance(sig.posonly("posonly"), sig.Argument)


@pytest.mark.usefixtures("testlogger")
def test_sig_magic() -> None:
    def foo(a: int, b: str, /, c: int = 1) -> None:
        pass

    @sig.from_function(foo)
    def bar():
        pass

    bar_sig = inspect.Signature.from_callable(bar)
    assert str(bar_sig) == "(a, b, /, c=1)"

    @sig.change_args(
        sig.posonly("some_posarg"),
        sig.arg("some_arg"),
        sig.kwarg("some_kwarg", None),
    )
    def baz(a, b, c) -> None:
        pass

    assert str(inspect.Signature.from_callable(baz)) == "(some_posarg, /, some_arg, some_kwarg=None)"
