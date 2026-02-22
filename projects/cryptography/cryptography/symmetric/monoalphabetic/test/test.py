import pytest
from cryptography.symmetric.monoalphabetic.caesar_shift import caesar_shift


def test_cryptogram_one():
    from cryptography.core.alphabet import Alphabet

    c = "L FDQQRW IRUHFDVW WR BRX WKH DFWLRQ RI UXVVLD LW LV D ULGGOH ZUDSSHQ \
        LQ D PBVWHUB LQVLGH DQ HQLJPD"
    plaintext_distribution = Alphabet()
    ciphertext_distribution = Alphabet()
    # This method is slightly overkill for this example
    # Looking at the text, we can guess that L and D must be
    # either A or I. There are 18 letters between L and D, and
    # 18 letters between I and A; therefore L == I and D == A
    # which implies i = -3 = 23
    # ... H I J K L M N ...
    # ... K L M N O P Q ...
    ciphertext_distribution.calculate_distribution(m=c)
    # plaintext_distribution.frequency_sort()
    # i = ciphertext_distribution.determine_i(m=ciphertext_distribution[0][0], c=plaintext_distribution[0][0])
    # plaintext_distribution.canonical_sort()
    ciphertext_distribution.canonical_sort()
    i = ciphertext_distribution.estimate_i_from_pdf(c=plaintext_distribution)
    assert i == 23
    m = caesar_shift(m=c, i=i, alphabet=ciphertext_distribution)
    assert (
        m
        == "ICANNOTFORECASTTOYOUTHEACTIONOFRUSSIAITISARIDDLEWRAPPENINAMYSTERYINSIDEANENIGMA"
    )


def test_cryptogram_two():
    from cryptography.core.alphabet import Alphabet

    c = "OXGB OBWB OBVB CNEBNL VTXLTK"
    plaintext_distribution = Alphabet()
    ciphertext_distribution = Alphabet()
    # This method is slightly overkill for this example
    # Looking at the text, we can guess that B must be a vowel
    # We can safely assume it is either E or I
    ciphertext_distribution.calculate_distribution(m=c)
    ciphertext_distribution.canonical_sort()
    i = ciphertext_distribution.estimate_i_from_pdf(c=plaintext_distribution)
    ciphertext_distribution.rotate(i)
    m = caesar_shift(m=c, i=i, alphabet=ciphertext_distribution)
    assert m == "VENIVIDIVICIJULIUSCAESAR"


def test_caesar_shift():
    c = caesar_shift(m="ABCD", i=1)
    assert c == "BCDE"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-s"]))
