import pytest
from cryptography.symmetric.caesar_shift import caesar_shift, determine_i
from cryptography.symmetric.vigenere import vigenere

def test_caesar_shift():
    c = caesar_shift(m="ABCD", i=1)
    assert c == "BCDE"
    i = determine_i(m="A", c="B")
    assert i == 1
    
def test_vigenere():
    c = vigenere(m="AbCd", key="aBc")
    assert c == "ACED"
    
if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-s"]))