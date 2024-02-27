class BufferDivider:
    @staticmethod
    def divide_bytes(buffer: bytes, slice_length: int) -> list:
        return [buffer[i: i + slice_length] for i in range(0, len(buffer), slice_length)]