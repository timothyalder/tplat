import pytest
from cryptography.symmetric.block.aes import aes


def test_aes():
    c = aes(m="0123456789ABCDEF")
    print(c)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-s"]))
