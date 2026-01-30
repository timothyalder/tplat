from typing import Union, List, Tuple
import math

from cryptography.core.alphabet import Alphabet

class ColumnMajorByteArray:
    
    def __init__(self, data: Union[bytes, str], shape: Tuple[int]):
        if isinstance(data, str):
            data = data.encode("utf-8")
        data = bytearray(data)
        self.shape = ColumnMajorByteArray._resolve_shape(len=len(data), shape=shape)
        pad_length = math.prod(shape) - len(data)
        self.data = ColumnMajorByteArray._pad(data=data, pad_length=pad_length)
        
    def __getitem__(self, *args):
        assert len(*args) == len(self.shape)
        idx = sum(tuple(i+p for i,p in zip(*args, self.shape)))
        return self.data[idx]
    
    def __str__(self):
        return(str(self.data))
    
    @staticmethod
    def _resolve_shape(len: int, shape: Tuple[int]) -> Tuple[int]:
        if -1 in shape:
            shape = list(shape)
            assert shape.count(-1) == 1, "Error! Only one ambiguous dimension may be passed to shape argument."
            shape[shape.index(-1)] = math.ceil(len / -math.prod(shape))
        return tuple(shape)
    
    @staticmethod
    def _pad(data: bytearray, pad_length: int, padding: bytes = b"\x00") -> bytearray:
        return data.extend(padding*pad_length)
        
        

def aes(m: str, alphabet: Union[List[str], List[Tuple[str, float]], Alphabet, None] = None):
    # 128-bit AES
    # Fixed block size of 128 bits
    # 4 rows by 4 cols of bytes (4x4*8=16*8=128-bits)
    m = ColumnMajorByteArray(data=m, shape=(-1,4,4))
    print(m)
    print(m.shape)
    
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