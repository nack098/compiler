class Node:
    def __init__(self):
        self.left = None
        self.right = None

    def set_left(self, value):
        self.left = value
    
    def set_right(self, value):
        self.right = value

    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()