Feature: Testing mini-wrapper for locals

    In this feature, the behavior of the mini-wrapper
    for locals will be tested.

    @bind
    Scenario: Testing Bind behavior
        Given we creating function and passing it to the context of the current scenario
        When we creating Bind object from received function locals
        Then we test Bind behavior
