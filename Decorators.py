"""Домашнее задание по тему Декораторы."""
import re
from typing import Any
import jsonschema


class InputParameterVerificationError(Exception):
    """Самописный Exception."""

    pass


class ResultVerificationError(Exception):
    """Самописный Exception."""

    pass


SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "type": "object",
    "examples": [
        {
            "key": 0
        }
    ],
    "required": [
        "key"
    ],
    "additionalProperties": False,
    "properties": {
        "key": {
            "type": "integer",
            "exclusiveMaximum": 100
        }
    }
}


# функция валидациии по регулярке
def input_func(validate_string: str) -> bool:
    """Функция для валидации по регулярному выражению."""
    string_verifier = re.compile("^[0-9]+$")
    if not string_verifier.match(validate_string):
        return False
    else:
        return bool(string_verifier.match(validate_string))


def result_func(result: dict) -> bool:
    """Функиця для валидации json."""
    try:
        if jsonschema.validate(result, SCHEMA) is None:
            return True
    except jsonschema.ValidationError:
        return False
    return True


def default_func() -> None:
    """Функция исполняемая по умолчанию."""
    print("Исполяемый код для функции default_func")


# decorator
def validate_data(func: Any, input_validation: Any = input_func,
                  result_validation: Any = result_func, on_fail_repeat_times: int = 1,
                  default_behavior: Any = default_func) -> Any:
    """Декоратор."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if input_validation(*args, **kwargs) is False:
            raise InputParameterVerificationError("Не прошла проверку на regex")
        else:
            result = func(*args, **kwargs)
            if result_validation(result) is False:
                if on_fail_repeat_times == 0:
                    if default_behavior is None:
                        raise ResultVerificationError("on-fail-repeat_times = 0")
                    else:
                        default_behavior()
                elif on_fail_repeat_times < 0:
                    while True:
                        result = result_validation(*args, **kwargs)
                        return result
                else:
                    for i in range(on_fail_repeat_times):
                        h = result_validation(*args, **kwargs)
                        if h is False:
                            print("Не прошла валидация по схеме " + str(result))
                    if default_behavior is None:
                        raise ResultVerificationError("Параметр on_fail_repeat_times is None")
                    else:
                        default_behavior()
        return result

    return wrapper


@validate_data
def target_function(argument: str) -> dict:
    """Целевая исполняемая функция."""
    return {"key": int(argument)}

# try:
#     print("Negative precondition case", target_function("ASDF"))
# except Exception as ex:
#     print(type(ex), str(ex))

# print("Positive case", target_function("12"))

# print("Negative postcondition case", target_function("123456"))
