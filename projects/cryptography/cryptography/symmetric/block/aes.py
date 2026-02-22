from typing import Union, List, Tuple

from cryptography.core.alphabet import Alphabet
from cryptography.core.array import ColumnMajorByteArray


def aes(
    m: str, alphabet: Union[List[str], List[Tuple[str, float]], Alphabet, None] = None
):
    # 128-bit AES
    # Fixed block size of 128 bits
    # 4 rows by 4 cols of bytes (4x4*8=16*8=128-bits)
    m = ColumnMajorByteArray(data=m, shape=(-1, 4, 4))
    print(m)
    print(m.shape)
    print(m.stride)
    print(m[0, 0])

    # 128-bit key
    # Key-size specifies number of transformation rounds
    # 128-bit key => 10 transformation rounds

    # KeyExpansion - derive the round keys (a 128-bit key for each round)
    # using the cipher key

    # Initial round key addition - combine each byte of the state with a byte of the
    # round key using bitwise XOR

    # 9 rounds of:
    #   - SubBytes: substitution according to Rinjdael S-box lookup table
    #   - ShiftRows: transposition of last three rows of state
    #   - MixColumns: linear mixing of columns of state
    #   - AddRoundKey

    # Final round:
    #   - SubBytes
    #   - ShiftRows
    #   - AddRoundKey


if __name__ == "__main__":
    m = "My Message" * 50
    print(len(m.encode("utf-8")))
    aes(m=m)
