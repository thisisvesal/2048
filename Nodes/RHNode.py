from .Node import Node

class RHNode:
    def __init__(self, node: Node) -> None:
        self.node = node
        self.row = node.row
        self.col = node.col
        self.next = None
        self.prev = None

    def get_tail(self):
        current = self
        while current.next != None:
            current = current.next
        return current