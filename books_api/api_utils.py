def cleanse_string(string: str) -> str:
    """
    Cleanses a string by stripping whitespace and converting it to lowercase.

    Args:
        string (str): The string to cleanse.
    Returns:
        str: The cleansed string.
    """
    return string.strip().casefold()


def is_casefold_match(field_value: str, query: str) -> bool:
    """Case-insensitive comparison with whitespace normalization."""
    return cleanse_string(field_value) == cleanse_string(query)


def is_positive_integer(input: int) -> bool:
    """
    Checks if the input is a positive integer.

    Args:
        input (int): The input to check.
    Returns:
        bool: True if the input is a positive integer, False otherwise.
    """
    return input > 0
