import pytest

from cryptography.core.alphabet import Alphabet

def test_alphabet():
    a = Alphabet()
    assert len(a) == 26
    assert (a[0][0] == "A") and ((a[0][1] - 0.0812) < 1e-6)
    a = Alphabet(alphabet=["A","B","C", "0", "1"])
    assert len(a) == 5
    a.rotate(1)
    assert (a[0][0] == "B") and ((a[0][1] - 0.0149) < 1e-6)
    a.frequency_sort()
    assert a.alphabet == ["A", "C", "B", "0", "1"]
    a.canonical_sort()
    assert a.alphabet == ["A", "B", "C", "0", "1"]
    
    
if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-s"]))