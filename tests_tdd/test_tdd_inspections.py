import pytest

from funchacks import inspections
from tests_tdd._tools import testlogger


@pytest.mark.usefixtures("testlogger")
def test_get_locals() -> None:
    def foo(a: int, b: int) -> int:
        c = 1
        d = 2
        return a + b + c + d

    foo_locals = inspections.getlocals(foo.__code__)
    assert hasattr(foo_locals, "asdict")

    assert isinstance(foo_locals, zip)
    assert dict(foo_locals) == {"c": 1, "d": 2}
