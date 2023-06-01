import re


def extract_ko(text: str) -> list[str]:
    """
    Extracts KO numbers from text
    :param text: str
    :return: list[str]
    """
    return re.findall(r'K\d{5}', text)


def extract_reaction(text: str) -> list[str]:
    """
    Extracts Reaction numbers from text
    :param text: str
    :return: list[str]
    """
    return re.findall(r'R\d{5}', text)


def extract_compound(text: str) -> list[str]:
    """
    Extracts Compound numbers from text
    :param text: str
    :return: list[str]
    """
    return re.findall(r'C\d{5}', text)


