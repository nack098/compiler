from .node import Node

class RootNode(Node):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return self.left
    
    def __repr__(self):
        return self.__str__()