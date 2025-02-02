class Node:
    def __init__(self, value: int, row: int, col: int) -> None:
        self.value = value
        self.row = row
        self.col = col
        self.up = None
        self.down = None
        self.left = None
        self.right = None

    def __repr__(self) -> str:
        return f"Node({self.value}, {self.row}, {self.col})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Node):
            return False
        
        return self.value == other.value and self.row == other.row and self.col == other.col
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def get_down_tail(self):
        """"Gets the last node in the down direction"""
        current = self
        while current.down != None:
            current = current.down
        return current
    
    def get_right_tail(self):
        """"Gets the last node in the right direction"""
        current = self
        while current.right != None:
            current = current.right
        return current
    
    def get_up_tail(self):
        """"Gets the last node in the up direction"""
        current = self
        while current.up != None:
            current = current.up
        return current

    def get_left_tail(self):
        """"Gets the last node in the left direction"""
        current = self
        while current.left != None:
            current = current.left
        return current