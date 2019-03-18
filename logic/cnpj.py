# cnpj function from
# https://github.com/luizberti/brutils

from itertools import chain
from dstr_common_lib.util import clear_punctuation


def display(cnpj):  # type: (str) -> str
    """
    Will format an adequately formatted numbers-only CNPJ string,
    adding in standard formatting visual aid symbols for display.
    """
    if not cnpj.isdigit() or len(cnpj) != 14 or len(set(cnpj)) == 1: return None
    return '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])


def hashdigit(cnpj, position):  # type: (str, int) -> int
    """
    Will compute the given `position` checksum digit for the `cnpj`
    input. The input needs to contain all elements previous to
    `position` else computation will yield the wrong result.
    """
    weightgen = chain(range(position -8, 1, -1), range(9, 1, -1))
    val = sum(int(digit) * weight for digit, weight in zip(cnpj, weightgen)) % 11
    return 0 if val < 2 else 11 - val


def checksum(basenum):  # type: (str) -> str
    """
    Will compute the checksum digits for a given CNPJ base number.
    `basenum` needs to be a digit-string of adequate length.
    """
    verifying_digits = str(hashdigit(basenum, 13))
    verifying_digits += str(hashdigit(basenum + verifying_digits, 14))
    return verifying_digits


def validate(_cnpj):  # type: (str) -> bool
    """
    Returns whether or not the verifying checksum digits of the
    given `cnpj` match it's base number. Input should be a digit
    string of proper length.
    """
    cnpj = clear_punctuation(_cnpj)
    if not cnpj.isdigit() or len(cnpj) != 14 or len(set(cnpj)) == 1: return False, None
    expected_hash = "".join([str(hashdigit(cnpj, i+13)) for i, v in enumerate(cnpj[12:])])
    return cnpj[12:] == expected_hash, display(cnpj[:12] + expected_hash)
