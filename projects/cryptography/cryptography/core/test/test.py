import pytest
import random

from cryptography.core.alphabet import Alphabet


def test_alphabet():
    a = Alphabet()
    assert len(a) == 26
    assert (a[0][0] == "A") and ((a[0][1] - 0.0812) < 1e-6)
    assert (a["a"][0] == "A") and ((a["A"][1] - 0.0812) < 1e-6)
    a = Alphabet(alphabet=["A", "B", "C", "0", "1"])
    assert len(a) == 5
    a.rotate(1)
    assert (a[0][0] == "B") and ((a[0][1] - 0.0149) < 1e-6)


def test_sort():
    a = Alphabet(alphabet=["A", "B", "C", "0", "1"])
    a.frequency_sort()
    assert a.alphabet == ["A", "C", "B", "0", "1"]
    a.canonical_sort()
    assert a.alphabet == ["A", "B", "C", "0", "1"]


def test_distribution():
    a = Alphabet()
    a.calculate_distribution(m="aAaCc")
    assert ((a["A"][1] - 0.6) < 1e-6) and ((a["b"][1] - 0.0) < 1e-6)
    assert a.alphabet[0:2] == [
        "A",
        "C",
    ]  # calculate_distribution() applies a frequency_sort()


def test_shift_calculation():
    a = Alphabet()
    c = Alphabet()
    i = 4
    c.rotate(i)
    assert a.determine_i(m=a[0][0], c=c[0][0]) == i
    c.probabilities = [prob + random.uniform(-0.005, 0.005) for prob in c.probabilities]
    integral = sum(c.probabilities)
    c.probabilities = [prob / integral for prob in c.probabilities]
    assert c.estimate_i_from_pdf(a) == i


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-s"]))
