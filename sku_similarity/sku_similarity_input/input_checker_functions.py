import re


def return_string(input) -> str:
    """Returns input as string

    Args:
        input (unknown): sku_code

    Returns:
        str: input as string
    """
    return str(input)


def remove_whitespace(input: str) -> str:
    """Remove whitespace as sku does not have white spaces

    Args:
        input (str): sku_code

    Returns:
        str: input without whitespaces
    """
    return input.replace(" ", "")


def to_lower_case(input: str) -> str:
    """transform input to lowerase

    Args:
        input (str): sku_code
    Returns:
        str: input as lowercase
    """
    return input.lower()


def check_sku_format(input: str) -> bool:
    """checks for correct sku format like sku-123
    regex explanation:
    match needs to start with "sku-" followed and ended by any number of digts

    Args:
        input (str): sku_code

    Raises:
        ValueError: Unvalid input if regex is does not match

    Returns:
        bool: True if format is correct
    """
    if re.match("sku-\d+$", input):
        return True
    else:
        raise ValueError(
            "Unvalid input -- check if your input is in the correct sku format (i.e. sku-123)"
        )


def apply_input_checking(input) -> str:
    """apply multiple preprocessing functions for the sku code

    Args:
        input (unknown): sku code

    Returns:
        str: formated sku code
    """
    sku_code = return_string(input)
    sku_code = remove_whitespace(sku_code)
    sku_code = to_lower_case(sku_code)
    check_sku_format(sku_code)
    return sku_code
