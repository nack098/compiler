from collections.abc import Iterable, Generator


class Result:

    res: Generator

    def __init__(self, res):
        self.res = res

    def unwrap(self):   
        return list(self.res)


class PipeLine():

    pipe_call: Iterable = []

    def __init__(self, *pipe_call: Iterable):
        self.pipe_call = pipe_call
    
    def __call__(self, value):
        res = value
        for func in self.pipe_call:
            res = func(res)
        return Result(res)