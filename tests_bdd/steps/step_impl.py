from __future__ import annotations

from typing import TYPE_CHECKING

from behave import given, then, use_fixture, when
from hamcrest import assert_that, equal_to, instance_of, is_not
from typing_extensions import TypeAlias

from funchacks import WrapFunction, make_wrap
from funchacks.internal import ZipGeneric
from tests_bdd._tools import function_template, has_args

if TYPE_CHECKING:
    _FirstContext: TypeAlias = object()
    _SecondContext: TypeAlias = object()
    _ThirdContext: TypeAlias = object()


@given("we have created function")
def step_adding_function_to_the_context(context: _FirstContext) -> None:
    """SCENARIO: 1

    Adding a function template to the context of
    the current scenario for further testing.
    """
    context.function = use_fixture(function_template, context)


@when("we creating WrapFunction object")
def step_creating_wrapfunction_object(context: _FirstContext) -> None:
    """SCENARIO: 1

    Create a WrapFunction object and do basic tests
    on it as an object.
    """
    wrap = WrapFunction.from_function(context.function)

    assert_that(wrap, is_not(None))
    assert_that(wrap, instance_of(WrapFunction))

    context.wrap = wrap


@then("we test created WrapFunction object")
def step_test_behavior_of_created_object(context: _FirstContext) -> None:
    """SCENARIO: 1

    We have created a Wrap Function object,
    now we will test its behavior and attributes.
    """
    wrap = context.wrap

    assert_that(wrap, has_args("flocals"))
    assert_that(wrap.flocals, instance_of(zip))


@given("we have created new WrapFunction object")
def step_creating_new_wrapfunction_object(context: _SecondContext) -> None:
    """SCENARIO: 2

    We created a new WrapFunction object and added
    it to the context of the current scenario.
    """
    context.new_wrap = WrapFunction.from_function(use_fixture(function_template, context))


@then("we test properties of created object")
def step_testing_properties_of_created_object(context: _SecondContext) -> None:
    """SCENARIO: 2

    We already have a WrapFunction object created,
    now we will test its properties.
    """
    new_wrap = context.new_wrap

    assert_that(new_wrap, is_not(None))
    assert_that(new_wrap, instance_of(WrapFunction))

    assert_that(new_wrap.flocals, instance_of(ZipGeneric))
    assert_that(dict(new_wrap.flocals), equal_to({"d": 1, "e": 2}))


@given("we have created some new function")
def step_creating_new_function(context: _ThirdContext) -> None:
    """SCENARIO: 3

    We already have an object of the created function,
    now we add it to the context of the current scenario
    for further testing.
    """
    context.function = use_fixture(function_template, context)


@when("we creating WrapFunction object using make_wrap function")
def step_creating_new_object_using_make_wrap(context: _ThirdContext) -> None:
    """SCENARIO: 3

    We created a WrapFunction object using the make_wrap
    function, now we do some basic tests of it as an object.
    """
    wrap = make_wrap(context.function)

    assert_that(wrap, is_not(None))
    assert_that(wrap, instance_of(WrapFunction))

    context.wrap = wrap


@then("we test make_wrap callback")
def step_testing_make_wrap_callback(context: _ThirdContext) -> None:
    """SCENARIO: 3

    We've created a WrapFunction object using the make_wrap
    function, tested its basic properties, now we'll partially
    test its behavior.
    """
    assert_that(context.wrap.flocals, instance_of(ZipGeneric))
    assert_that(dict(context.wrap.flocals), equal_to({"d": 1, "e": 2}))
