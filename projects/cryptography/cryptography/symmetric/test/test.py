import pytest
from cryptography.symmetric.caesar_shift import caesar_shift
from cryptography.symmetric.vigenere import vigenere


def cryptogram_one():
    from cryptography.core.alphabet import Alphabet

    c = "L FDQQRW IRUHFDVW WR BRX WKH DFWLRQ RI UXVVLD LW LV D ULGGOH ZUDSSHQ LQ D PBVWHUB LQVLGH DQ HQLJPD"
    a = Alphabet()
    a.calculate_distribution(m=c)
    m = caesar_shift(m=c, i=a.estimate_i_from_pdf())
    print(m)
    assert m[0] == "I"


def test_caesar_shift():
    c = caesar_shift(m="ABCD", i=1)
    assert c == "BCDE"


def test_vigenere():
    c = vigenere(m="AbCd", key="aBc")
    assert c == "ACED"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-s"]))
