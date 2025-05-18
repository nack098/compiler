from collections.abc import Iterable
from .end_node import EndNode
from .node import Node
from .op_node import OpNode
from .root_node import RootNode
from .start_node import StartNode
from .oprnd_node import OprndNode

class AST:

    parser: Iterable = []
    start: Node = None
    current_node: Node = None

    def __init__(self):
        pass

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            curr = next(self.parser)
            match curr:
                case "asm":
                    node = StartNode()
                    if self.current_node:
                        if type(self.current_node.tail()) is EndNode:
                            self.current_node.set_left(node)
                        else:
                            self.current_node.set_right(node)
                        self.current_node = node
                    else:
                        self.start = node
                        self.current_node = node
                case "e":
                    node = EndNode()
                    self.current_node.set_right(node)
                case "op":
                    node = OpNode()
                    self.current_node.set_right(node)
                    self.current_node = node
                case "oprnd" | "param":
                    node = OprndNode()
                    self.current_node.set_right(node)
                    self.current_node = node
                case "CLRA" | "MOV" | "ADD" | "MOVA" | "R1" | "R2" | "100" | "200":
                    node = RootNode()
                    node.set_left(curr)
                    self.current_node.set_left(node)
            return self.current_node
        except StopIteration:
            raise StopIteration

    def __call__(self, parser: Iterable):
        self.parser = parser
        self.start = None
        self.current_node = None
        return self