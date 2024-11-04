import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from password_checker import check_length, check_char_types, is_common_password


def test_check_length():
    assert check_length("abc123!") == False
    assert check_length("abcABC123!") == True


def test_check_char_types():
    assert check_char_types("password") == False
    assert check_char_types("PASSWORD1") == False
    assert check_char_types("password1") == False
    assert check_char_types("Password!") == False


def test_is_common_password():
    assert is_common_password("123456") == True
    assert is_common_password("uniquePassword123!") == False


def test_check_length_edge_cases():
    assert check_length("") == False  # Empty string
    assert check_length("1234567890abcdef") == True  # Long password


def test_check_char_types_edge_cases():
    assert check_char_types("ONLYUPPERCASE") == False
    assert check_char_types("123456") == False
    assert check_char_types("!!!!!!") == False
    assert check_char_types("1234AB!") == False  # Missing lowercase
