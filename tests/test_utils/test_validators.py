import pytest
from pydantic import ValidationError
from pydantic.main import BaseModel

from app.utils.validators import NonEmptyString


@pytest.mark.parametrize(
    "input_value,expect_error",
    [
        ("    ", True),
        ("\t\t\t", True),
        ("\t\t\t   ", True),
        (" Valid", False),
        ("Valid ", False),
        (" Valid  ", False),
        ("", False),
    ],
)
def test_non_empty_string(input_value: str, expect_error: bool) -> None:
    class Person(BaseModel):
        first_name: NonEmptyString

    data = {"first_name": input_value}

    if expect_error:
        with pytest.raises(ValidationError):
            Person.model_validate(data)
    else:
        person = Person.model_validate(data)
        assert person.first_name == input_value.strip()
