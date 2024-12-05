import random
from Nodes.RHNode import RHNode
from Nodes.Node import Node

class Grid:
    def __init__(self, size: int, prev=None) -> None:
        if size < 2:
            print("Grid: __init__: Grid size must be at least 2")
            return

        self.size = size
        self.cellsStatus = [[False for _ in range(size)] for _ in range(size)]
        self.rowsHead = None  # Head of the rows' linked list
        self.colsHead = None  # Head of the columns' linked list
        self.prev = prev  # Previous grid in a linked list of grids
        self.next = None  # Next grid in a linked list of grids
        self.score = 0

    def __repr__(self):
        ans = ""
        ans += f"Score: {self.score}\n"
        for i in range(self.size):
            for j in range(self.size):
                node = self.getNode(i, j)
                if node == None:
                    ans += "- "
                else:
                    ans += f"{node.value} "
            ans += "\n"

        return ans

    def moveNodeTo(self, node, row, column):
        """Moves a given node to the specified row and column."""
        # Remove the node from its current position
        # self.removeNode(node)

        # self.removeEmptyColumns()
        # self.removeEmptyRows()

        # Place it at the new position
        node.row = row
        node.col = column
        # self.addNode(node)

    def moveNodeToColumn(self, node, column):
        """Moves a given node to a specific column."""
        self.removeNode(node)
        node.col = column
        self.addNode(node)
    
    def removeEmptyColumns(self):
        """Removes all empty columns."""
        current = self.colsHead
        prev = None
        while current:
            if current.node is None: 
                if prev:
                    prev.next = current.next
                else:
                    self.colsHead = current.next 
            else:
                prev = current 
            current = current.next 

    def removeEmptyRows(self):
        """Removes all empty rows."""
        current = self.rowsHead
        prev = None
        while current:
            if current.node is None:
                if prev:
                    prev.next = current.next
                else:
                    self.rowsHead = current.next
            else:
                prev = current
            current = current.next

    def removeNode(self, node):
        """Removes a node from the grid."""
        if node.up:
            node.up.down = node.down
        if node.down:
            node.down.up = node.up
        if node.left:
            node.left.right = node.right
        if node.right:
            node.right.left = node.left

        column = self.getColHead(node.col)
        if column.node == node:
            column.node = node.down

        row = self.getRowHead(node.row)
        if row.node == node:
            row.node = node.right

    def addNode(self, node):
        """Adds a node to the grid."""
        # Add to the row header list
        row_node = self.getRowHead(node.row)
        if not row_node:
            # Create a new row header and insert it in the correct position
            new_row = RHNode(node)
            if not self.rowsHead or self.rowsHead.node.row > node.row:
                # Insert at the beginning
                new_row.next = self.rowsHead
                self.rowsHead = new_row
            else:
                # Traverse to find the correct position
                current = self.rowsHead
                while current.next and current.next.node.row < node.row:
                    current = current.next
                new_row.next = current.next
                current.next = new_row
        else:
            # Add node to the existing row
            tail = row_node.node.get_right_tail()
            tail.right = node
            node.left = tail

        # Add to the column header list
        col_node = self.getColHead(node.col)
        if not col_node:
            # Create a new column header and insert it in the correct position
            new_col = RHNode(node)
            if not self.colsHead or self.colsHead.node.col > node.col:
                # Insert at the beginning
                new_col.next = self.colsHead
                self.colsHead = new_col
            else:
                # Traverse to find the correct position
                current = self.colsHead
                while current.next and current.next.node.col < node.col:
                    current = current.next
                new_col.next = current.next
                current.next = new_col
        else:
            # Add node to the existing column
            tail = col_node.node.get_down_tail()
            tail.down = node
            node.up = tail


    def getNode(self, row, column):
        """Retrieves a node from the grid by its position."""
        current = self.rowsHead
        while current:
            if current.node.row == row:
                node = current.node
                while node and node.col != column:
                    node = node.right
                return node
            current = current.next
        return None

    def moveUp(self):
        """Moves all nodes up in their respective columns."""
        col = self.colsHead
        while col:
            current = col.node
            row = 0
            while current:
                self.moveNodeTo(current, row, current.col)
                row += 1
                current = current.down
            col = col.next

    def moveDown(self):
        """Moves all nodes down in their respective columns."""
        col = self.colsHead
        while col:
            current = col.node.get_down_tail()
            row = self.size - 1
            while current:
                self.moveNodeTo(current, row, current.col)
                row -= 1
                current = current.up
            col = col.next

    def moveLeft(self):
        """Moves all nodes left in their respective rows."""
        row = self.rowsHead
        while row:
            current = row.node
            col = 0
            while current:
                self.moveNodeTo(current, current.row, col)
                col += 1
                current = current.right
            row = row.next

    def moveRight(self):
        """Moves all nodes right in their respective rows."""
        row = self.rowsHead
        while row:
            current = row.node.get_right_tail()
            col = self.size - 1
            while current:
                self.moveNodeTo(current, current.row, col)
                col -= 1
                current = current.left
            row = row.next

    def move(self, direction):
        if direction == "up" or direction == "w":
            self.moveUp()
        elif direction == "left" or direction == "a":
            self.moveLeft()
        elif direction == "down" or direction == "s":
            self.moveDown()
        elif direction == "right" or direction == "d":
            self.moveRight()

    def merge(self, one: Node, other: Node) -> None:
        one.value += other.value
        self.score += one.value
        self.removeNode(other)

    def getRowHead(self, row):
        """Returns the head node of a specific row."""
        current = self.rowsHead
        while current:
            if current.node.row == row:
                return current
            current = current.next
        return None

    def getColHead(self, column):
        """Returns the head node of a specific column."""
        current = self.colsHead
        while current:
            if current.node.col == column:
                return current
            current = current.next
        return None
