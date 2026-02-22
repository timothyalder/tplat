from typing import List


def vectorise(m: str, n: int) -> List[int]:
    assert n >= 256, "Error! n is too small - pick larger prime numbers"
    b = m.encode("utf-8")
    k = (n.bit_length() - 1) // 8
    return [int.from_bytes(b[i : i + k], "big") for i in range(0, len(b), k)]
