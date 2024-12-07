from .Node import Node

class RHNode:
    def __init__(self, node: Node) -> None:
        self.node = node
        self.next = None

    def __repr__(self):
        ans = ""
        current = self
        while current.next != None:
            ans += current.node.__repr__() + " -> "
        ans += current.node.__repr__()
        return ans