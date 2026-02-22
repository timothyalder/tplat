from typing import Union, Tuple, Optional
import math


class ColumnMajorByteArray:

    def __init__(
        self,
        data: Union[bytes, str],
        shape: Tuple[int],
        stride: Optional[Tuple[int]] = None,
    ):
        if isinstance(data, str):
            data = data.encode("utf-8")
        data = bytearray(data)
        self.shape = ColumnMajorByteArray._resolve_shape(len=len(data), shape=shape)
        self.ndim = len(self.shape)
        self.stride = (
            stride
            if stride is not None
            else ColumnMajorByteArray._resolve_stride(shape=self.shape)
        )
        pad_length = math.prod(shape) - len(data)
        self.data = ColumnMajorByteArray._pad(data=data, pad_length=pad_length)

    def __getitem__(self, idx) -> bytearray:
        if not isinstance(idx, tuple):
            idx = (idx,)

        if len(idx) > self.ndim:
            raise IndexError("Too many indices")

        for i, d in zip(idx, self.shape):
            if not (0 <= i < d):
                raise IndexError("Index out of bounds")

        offset = sum(i * s for i, s in zip(idx, self.stride))

        if len(idx) == self.ndim:
            return self.data[offset]

        span = math.prod(self.shape[len(idx) :])
        return self.data[offset : offset + span]

    def __setitem__(self, idx, val) -> None:
        if not isinstance(idx, tuple):
            idx = (idx,)

        if len(idx) != self.ndim:
            raise IndexError("Assignment requires full indexing")

        for i, d in zip(idx, self.shape):
            if not (0 <= i < d):
                raise IndexError("Index out of bounds")

        offset = sum(i * s for i, s in zip(idx, self.stride))
        self.data[offset] = val

    def __len__(self) -> int:
        return self.shape[0]

    def __str__(self) -> str:
        return str(self.data)

    @staticmethod
    def _resolve_shape(len: int, shape: Tuple[int]) -> Tuple[int]:
        if -1 in shape:
            shape = list(shape)
            assert (
                shape.count(-1) == 1
            ), "Error! Only one ambiguous dimension may be passed to shape argument."
            shape[shape.index(-1)] = math.ceil(len / -math.prod(shape))
        return tuple(shape)

    @staticmethod
    def _resolve_stride(shape: Tuple[int]) -> Tuple[int]:
        strides = [1] * len(shape)
        strides[-1] = 1
        strides[-2] = shape[-1]
        for i in range(len(shape) - 3, -1, -1):
            strides[i] = strides[i + 1] * shape[i + 1]
        return tuple(strides)

    @staticmethod
    def _pad(data: bytearray, pad_length: int, padding: bytes = b"\x00") -> bytearray:
        data.extend(padding * pad_length)
        return data
