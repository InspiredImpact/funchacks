Feature: Testing WrapFunction object

    In this feature we will test the main methods and
    properties of the WrapFunction class.

    @main
    Scenario: Testing WrapFunction object
        Given we have created function
        When we creating WrapFunction object
        Then we test created WrapFunction object

    @properties
    Scenario: Testing WrapFunction properties
        Given we have created new WrapFunction object
        Then we test properties of created object

    @make_wrap
    Scenario: Testing make_wrap function
        Given we have created some new function
        When we creating WrapFunction object using make_wrap function
        Then we test make_wrap callback
