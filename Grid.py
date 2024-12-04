import random
from Nodes.RHNode import RHNode
from Nodes.Node import Node

class Grid:
    def __init__(self, size: int) -> None:
        self.cellsStatus = [[False for _ in range(size)] for _ in range(size)]
        if size < 2:
            print("Grid: __init__: Grid size must be at least 2")
            return
        self.size = size
        self.rowsHead = None
        self.colsHead = None

    # Creates a row
    def _add_row(self, node: Node) -> None:
        if self._row_exists(node.row):
            return
        
        if self.rowsHead == None:
            self.rowsHead = RHNode(Node(node.value, node.row, 0))
            return
        
        current = self.rowsHead
        while current.next != None and current.next.row < node.row:
            current = current.next

        if current == None:
            print("Grid: _add_row: None row found")
            return
        
        if current.row == node.row:
            print("Grid: _add_row: Row already exists but undetected")
            return
        
        new = RHNode(Node(node.value, node.row, 0))
        current.next = new

    def _remove_row(self, row: int):
        if not self._row_exists(row):
            return
        
        if self.rowsHead.row == row:
            self.rowsHead = self.rowsHead.next
            return
        
        current = self.rowsHead
        while current.next != None and current.next.row != row:
            current = current.next
        
        if current.next == None:
            print("Grid: _remove_row: Nonexisting row undetected by _row_exists")
            return
        
        current.next = current.next.next

    def _row_exists(self, row: int):
        current = self.rowsHead
        while current != None:
            if current.row == row:
                return True
            current = current.next
        return False
    
    def _add_col(self, node: Node) -> None:
        if self._col_exists(node.col):
            return
        
        if self.colsHead == None:
            self.colsHead = RHNode(Node(node.value, 0, node.col))
            return
        
        current = self.colsHead
        while current.next != None and current.next.col < node.col:
            current = current.next

        if current == None:
            print("Grid: _add_col: None column found")
            return
        
        if current.col == node.col:
            print("Grid: _add_col: Column already exists but undetected")
            return
        
        new = RHNode(Node(node.value, 0, node.col))
        current.next = new

    def _remove_col(self, col: int):
        if not self._col_exists(col):
            return
        
        if self.colsHead.col == col:
            self.colsHead = self.colsHead.next
            return
        
        current = self.colsHead
        while current.next != None and current.next.col != col:
            current = current.next
        
        if current.next == None:
            print("Grid: _remove_col: Nonexisting column undetected by _col_exists")
            return
        
        current.next = current.next.next

    def _col_exists(self, col: int):
        current = self.colsHead
        while current != None:
            if current.col == col:
                return True
            current = current.next
        return False
    
    def _get_row(self, row: int) -> RHNode:
        current = self.rowsHead
        while current != None:
            if current.row == row:
                return current
            current = current.next
        return None
    
    def _get_col(self, col: int) -> RHNode:
        current = self.colsHead
        while current != None:
            if current.col == col:
                return current
            current = current.next
        return None
    
    def _add_node_to_row(self, node: Node):
        if not self._row_exists(node.row):
            self._add_row(node)
            return
        
        head = self._get_row(node.row)

        # Debug
        if head == None:
            print("Grid: _add_node_to_row: None head found")
            return
        if head.node == None:
            print("Grid: _add_node_to_row: None row head node found")
            return
        if head.node.value == 0:
            print("Grid: _add_node_to_row: Head node value is 0")
            return
        
        current = head.node

        if node.col < current.col: # Insert new at the beginning
            current.left = node
            node.right = current
            head.node = node
            return
        
        while current.right != None and current.right.col < node.col:
            current = current.right
        
        # Debug
        if current.col == node.col:
            print("Grid: _add_node_to_row: Node already exists in the new location but undetected")
            return
        

        if current.right != None:
            current.right.left = node
        node.right = current.right
        node.left = current
        current.right = node

    def _add_node_to_col(self, node: Node):
        if not self._col_exists(node.col):
            self._add_col(node)
            return
        
        head = self._get_col(node.col)

        # Debug
        if head == None:
            print("Grid: _add_node_to_col: None head found")
            return
        if head.node == None:
            print("Grid: _add_node_to_col: None column head node found")
            return
        if head.node.value == 0:
            print("Grid: _add_node_to_col: Head node value is 0")
            return
        
        current = head.node

        if node.row < current.row: # Insert new at the beginning
            current.up = node
            node.down = current
            head.node = node
            return
        
        while current.down != None and current.down.row < node.row:
            current = current.down
        
        # Debug
        if current.row == node.row:
            print("Grid: _add_node_to_col: Node already exists in the new location but undetected")
            return
        

        if(current.down != None):
            current.down.up = node
        node.down = current.down
        node.up = current
        current.down = node

    def _remove_node_from_row(self, node: Node) -> None:
        if not self._row_exists(node.row):
            return
        
        head = self._get_row(node.row)

        # Debug
        if head == None:
            print("Grid: _remove_node_from_row: None head found")
            return
        if head.node == None:
            print("Grid: _remove_node_from_row: None row head node found")
            return
        if head.node.value == 0:
            print("Grid: _remove_node_from_row: Head node value is 0")
            return
        
        current = head.node
        while current != None and current.col != node.col:
            current = current.right
        
        # Debug
        if current == None:
            print("Grid: _remove_node_from_row: node doesn't exist in the row")
            return
        
        if current.left == None:
            head.node = current.right
            if head.node == None:
                self._remove_row(node.row)
            return
        
        current.left.right = current.right
        if current.right != None:
            current.right.left = current.left


    def _remove_node_from_col(self, node: Node) -> None:
        if not self._col_exists(node.col):
            return
        
        head = self._get_col(node.col)

        # Debug
        if head == None:
            print("Grid: _remove_node_from_col: None head found")
            return
        if head.node == None:
            print("Grid: _remove_node_from_col: None column head node found")
            return
        if head.node.value == 0:
            print("Grid: _remove_node_from_col: Head node value is 0")
            return
        
        current = head.node
        while current != None and current.row != node.row:
            current = current.down
        
        # Debug
        if current == None:
            print("Grid: _remove_node_from_col: node doesn't exist in the column")
            return
        
        if current.up == None:
            head.node = current.down
            if head.node == None:
                self._remove_col(node.col)
            return
        
        current.up.down = current.down
        if current.down != None:
            current.down.up = current.up


    def add_node(self, node: Node) -> None:
        self._add_node_to_row(node)
        self._add_node_to_col(node)

    def remove_node(self, node: Node) -> None:
        self._remove_node_from_row(node)
        self._remove_node_from_col(node)

    def get(self, row: int, col: int) -> Node:
        if not self._row_exists(row) or not self._col_exists(col):
            return None
        
        head = self._get_row(row)
        current = head.node
        while current != None and current.col != col:
            current = current.right
        
        return current
    
    def _update_cells_status(self) -> None:
        for i in range(self.size):
            for j in range(self.size):
                self.cellsStatus[i][j] = (self.get(i, j) != None)

    def get_random_empty_cell(self) -> tuple:
        self._update_cells_status()
        empty = []

        for i in range(self.size):
            for j in range(self.size):
                if not self.cellsStatus[i][j]:
                    empty.append((i, j))

        if len(empty) == 0:
            return None
        
        return empty[random.randint(0, len(empty) - 1)]