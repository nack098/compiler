from typing import Literal
from collections.abc import Iterable


from .os_linux import Linux


class ExecutableGenerator:
    def __init__(self, os: Literal["windows", "linux"] = "linux"):
        match os:
            case "windows":
                raise NotImplementedError("windows build is not yet implemented")
            case "linux":
                self.os = Linux()
            case _:
                raise ValueError("unknown os")
    
    def __call__(self, code: Iterable):
        return self.os(code)