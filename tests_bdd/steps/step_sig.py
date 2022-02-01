from __future__ import annotations

import ast
from typing import TYPE_CHECKING

from behave import given, then, use_fixture, when
from hamcrest import assert_that, instance_of
from typing_extensions import TypeAlias

from funchacks import sig
from tests_bdd._tools import function_template, has_args

if TYPE_CHECKING:
    _FirstContext: TypeAlias = object()
    _SecondContext: TypeAlias = object()


@given("we have argument {name}, {default} and {type} of the argument")
def step_args_intro(context: _FirstContext, name: str, default: str, type: str) -> None:
    """SCENARIO: 1

    We have the name, default and type attributes, which we
    will later use to create the Argument object.
    """
    context.name = name
    context.type = type
    context.default = default


@when("we create argument with appropriate values")
def step_creating_arguments(context: _FirstContext) -> None:
    """SCENARIO: 1

    We take the previously received parameters from the context
    and create Argument objects.
    """
    args = (context.name, context.type)
    if context.default != "MISSING":
        argument = sig.Argument(
            *args,
            default=ast.literal_eval(context.default),
        )
    else:
        argument = sig.Argument(
            *args,
        )

    context.argument = argument
    assert_that(argument, has_args("name", "default", "type"))


@then("we will check their behavior")
def step_checking_arguments_behavior(context: _FirstContext) -> None:
    """SCENARIO: 1

    We test the behavior of the previously created
    Argument objects.
    """
    assert_that(context.argument, has_args("__dataclass_fields__"))  # is_dataclass


@then("additionally test the arg, kwarg, posonly and kwonly functions")
def step_testing_other_wrap_functions(_: _FirstContext) -> None:
    """SCENARIO: 1

    We additionally test functions such as arg, kwarg,
    posonly and kwonly.
    """
    assert_that(sig, has_args("arg", "kwarg", "posonly", "kwonly"))

    assert_that(sig.arg("some_argname"), instance_of(sig.Argument))
    assert_that(sig.kwarg("kwarg", None), instance_of(sig.Argument))
    assert_that(sig.posonly("posonly"), instance_of(sig.Argument))
    assert_that(sig.kwonly("kwonly", 1), instance_of(sig.Argument))


@given("we have some {decorator} name")
def step_passing_decorator_name(context: _SecondContext, decorator: str) -> None:
    """SCENARIO: 2

    Getting the name of the decorator and add it to
    the context of the current scenario.
    """
    context.decorator_name = decorator


@when("we pass function to the context of the current scenario")
def step_finalize_context(context: _SecondContext) -> None:
    """SCENARIO: 2

    Gettin the current decorator and adding it to
    the context of the current scenario.
    """
    context.function = use_fixture(function_template, context)
    context.decorator = getattr(sig, context.decorator_name)


@then("we test the behavior of this decorator")
def step_checking_behavior_of_decorator(context: _SecondContext) -> None:
    """SCENARIO: 2

    Testing the behavior of the received decorator
    from the context.
    """
    assert callable(context.decorator)
