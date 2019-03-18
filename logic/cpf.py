# cnpj function from
# https://github.com/luizberti/brutils

from itertools import chain
from dstr_common_lib.util import clear_punctuation


def display(cpf):  # type: (str) -> str
    """
    Will format an adequately formatted numbers-only CPF string,
    adding in standard formatting visual aid symbols for display.
    """
    if not cpf.isdigit() or len(cpf) != 11 or len(set(cpf)) == 1: return None
    return '{}.{}.{}-{}'.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])


def hashdigit(cpf, position):  # type: (str, int) -> int
    """
    Will compute the given `position` checksum digit for the `cpf`
    input. The input needs to contain all elements previous to
    `position` else computation will yield the wrong result.
    """
    val = sum(int(digit) * weight for digit, weight in zip(cpf, range(position, 1, -1))) % 11
    return 0 if val < 2 else 11 - val


def checksum(basenum):  # type: (str) -> str
    """
    Will compute the checksum digits for a given CPF base number.
    `basenum` needs to be a digit-string of adequate length.
    """
    verifying_digits = str(hashdigit(basenum, 10))
    verifying_digits += str(hashdigit(basenum + verifying_digits, 11))
    return verifying_digits


def validate(_cpf):  # type: (str) -> bool
    """
    Returns whether or not the verifying checksum digits of the
    given `cpf` match it's base number. Input should be a digit
    string of proper length.
    """
    cpf = clear_punctuation(_cpf)
    if not cpf.isdigit() or len(cpf) != 11 or len(set(cpf)) == 1: return False, None
    expected_hash = "".join([str(hashdigit(cpf, i +10)) for i, v in enumerate(cpf[9:])])
    return cpf[9:] == expected_hash, display(cpf[:9] + expected_hash)
