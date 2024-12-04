from .Node import Node

class RHNode:
    def __init__(self, node: Node) -> None:
        self.node = node
        self.row = node.row
        self.col = node.col
        self.next = None