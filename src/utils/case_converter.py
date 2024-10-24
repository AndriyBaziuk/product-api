import re


def camel_case_to_snake_case(input_str: str) -> str:
    pattern = re.compile(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")
    return pattern.sub("_", input_str).lower()
