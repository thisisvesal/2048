from .Node import Node

class RHNode:
    def __init__(self, node: Node) -> None:
        self.node = node
        self.next = None

    def get_tail(self):
        current = self
        while current.next != None:
            current = current.next
        return current