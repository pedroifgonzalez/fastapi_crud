from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema


class NonEmptyString:
    """Custom type that ensures a string is not only whitespace nor tabs."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: str, handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate, core_schema.str_schema()
        )

    @classmethod
    def _validate(cls, input_value: str, /) -> str:
        if not len(input_value):
            return input_value
        len_input = len(input_value)
        only_whitespaces = len_input == input_value.count(" ")
        only_tabs = len_input == input_value.count("\t")
        mix_tabs_whitespaces = len_input == input_value.count(" ") + input_value.count(
            "\t"
        )
        empty_str = only_tabs or only_whitespaces or mix_tabs_whitespaces
        if empty_str is True:
            raise PydanticCustomError(
                "empty_string", "String field has no chars except spaces or tabs"
            )
        return input_value.strip()
