from __future__ import annotations

from typing import TYPE_CHECKING, Any, Hashable, TypeVar

from behave import given, then, when
from hamcrest import assert_that, calling, equal_to, instance_of, raises

from funchacks import inspections, sig
from funchacks.errors import TemporaryError

if TYPE_CHECKING:
    _FirstContextT = TypeVar("_FirstContextT")


@given("we creating function and passing it to the context of the current scenario")
def step_creating_function_with_locals(context: _FirstContextT) -> None:
    """SCENARIO: 1

    Creating function object for further tests.
    """

    def foo() -> None:
        a = 1
        b = 2
        return None

    context.function = foo


@when("we creating Bind object from received function locals")
def step_creating_bind_object(context: _FirstContextT) -> None:
    """SCENARIO: 1

    Creating wrapper over function locals.
    """
    localvars = inspections.getlocals(context.function.__code__).asdict()

    @sig.change_args(sig.posonly("a"))
    def baz(*args: Any) -> sig.Bind[Hashable, Any]:
        return sig.Bind.from_locals(localvars, in_=baz)

    @sig.change_args(sig.kwonly("b"))
    def bazz(**kwargs: Any) -> sig.Bind[Hashable, Any]:
        return sig.Bind.from_locals(localvars, in_=baz)

    assert_that(calling(baz).with_args(None), raises(TemporaryError))
    assert_that(calling(bazz).with_args(b=None), raises(TemporaryError))
    """Posonly and kwonly args don't supports yet, only in signature."""

    @sig.change_args(
        sig.arg("a"),
        sig.kwarg("b", None),
    )
    def bar(*args: Any, **kwargs: Any) -> sig.Bind[Hashable, Any]:
        return sig.Bind.from_locals(localvars, in_=bar)

    context.lvars = bar(None)


@then("we test Bind behavior")
def step_testing_wrapper_behavior(context: _FirstContextT) -> None:
    """SCENARIO: 1

    Testing wrapper behavior.
    """
    lvars = context.lvars

    assert_that(lvars, instance_of(sig.Bind))
    assert_that(lvars.initial, instance_of(dict))
    assert_that(lvars.initial, equal_to({"a": 1, "b": 2}))

    assert_that(lvars.args(), equal_to(["a"]))
    assert_that(lvars.kwargs(), equal_to(["b"]))

    assert_that(lvars.get("a"), equal_to(1))
    assert_that(lvars.get("b", equal_to(2)))
