from os import chmod
from collections.abc import Iterable
from dataclasses import dataclass


@dataclass
class Headers:
    elf_header = (
        b"\x7fELF"
        b"\x02"
        b"\x01"
        b"\x01"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x02\x00"
        b"\x3e\x00"
        b"\x01\x00\x00\x00"
        b"\x78\x00\x40\x00\x00\x00\x00\x00"
        b"\x40\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00"
        b"\x40\x00"
        b"\x38\x00"
        b"\x01\x00"
        b"\x00\x00"
        b"\x00\x00"
        b"\x00\x00"
    )

    program_header = (
        b"\x01\x00\x00\x00"
        b"\x05\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x40\x00\x00\x00\x00\x00"
        b"\x00\x00\x40\x00\x00\x00\x00\x00"
        b"\x78\x00\x00\x00\x00\x00\x00\x00"
        b"\x78\x00\x00\x00\x00\x00\x00\x00"
        b"\x05\x00\x00\x00"
        b"\x00\x10\x00\x00"
    )

    ret_code = (
        b"\xb8\x3c\x00\x00\x00"
        b"\x31\xff"
        b"\x0f\x05"
    )


class Linux:
    def __call__(self, code: Iterable):
        with open("a.out", "wb") as file:
            total_size = len(Headers.elf_header) + len(Headers.program_header)
            file.write(Headers.elf_header)
            file.write(Headers.program_header)
            for bytes_code in code:
                total_size += len(bytes_code)
                file.write(bytes_code)
            total_size += len(Headers.ret_code)
            file.write(Headers.ret_code)
            chmod("a.out", 0o700)
            print("Done")
            return [total_size]