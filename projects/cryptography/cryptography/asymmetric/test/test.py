import pytest

from cryptography.asymmetric.rsa import encrypt, decrypt, bruteforce


def test_bruteforce():
    m = "Hello World"
    p = 61
    q = 53
    c, d = encrypt(m=m, p=p, q=q)
    possible_m, _ = bruteforce(c=c, d=d)
    assert m in possible_m


def test_rsa():
    m = "Hello World"
    p = 61
    q = 53
    c, d = encrypt(m=m, p=p, q=q)
    print(f"Ciphertext: '{c}'")
    assert c == [2695, 2228, 562, 562, 1270, 2358, 856, 1270, 968, 562, 1605]
    assert decrypt(c=c, p=p, q=q, d=d) == "Hello World"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-s"]))
