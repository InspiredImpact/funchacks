Feature: Testing sig utils

    In this feature, we will test all the features
    and behavior of funchacks.sig.

    @wraps
    Scenario Outline: sig wraps
        Given we have argument <name>, <default> and <type> of the argument
        When we create argument with appropriate values
        Then we will check their behavior

        Examples:
            | name    | default  | type |
            | arg     |  MISSING | 1    |
            | kwarg   |   None   | 1    |
            | posonly |  MISSING | 0    |
            | kwonly  |  MISSING | 3    |

    @decorator @change_args @from_function
    Scenario Outline: change_args decorator
        Given we have some <decorator> name
        When we pass function to the context of the current scenario
        Then we test the behavior of this decorator
        And additionally test the arg, kwarg, posonly and kwonly functions

    Examples:
        | decorator     |
        | change_args   |
        | from_function |
