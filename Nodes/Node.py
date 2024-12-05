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
    
    def __eq__(self, value) -> bool:
        if value is not Node:
            return False
        
        return self.value == value.value and self.row == value.row and self.col == value.col
    
    def get_bottom_tail(self):
        current = self
        while current.down != None:
            current = current.down
        return current
    
    def get_right_tail(self):
        current = self
        while current.right != None:
            current = current.right
        return current