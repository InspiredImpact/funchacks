import pytest

from funchacks.internal import ZipGeneric, FilterGeneric
from tests_tdd._tools import testlogger


@pytest.mark.usefixtures("testlogger")
def test_generics() -> None:
    assert issubclass(ZipGeneric, zip)
    assert issubclass(FilterGeneric, filter)
