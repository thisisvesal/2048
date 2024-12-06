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
        self.removeNode(node)
        # print(f"{node} removed")
        # print(self)

        # Place it at the new position
        node.row = row
        node.col = column
        # print(f"{node} added")
        self.addNode(node)
        # print(self)

    def moveNodeToColumn(self, node, column):
        """Moves a given node to a specific column."""
        self.removeNode(node)
        node.col = column
        self.addNode(node)

    def removeColumn(self, col):
        if self.getColHead(col) == None:
            return
        if self.colsHead.node.col == col:
            self.colsHead = self.colsHead.next
            return
        current = self.colsHead
        while current.next and current.next.node.col != col:
            current = current.next
        if current.next == None:
            return
        
        current.next = current.next.next

    def removeRow(self, row):
        if self.getRowHead(row) == None:
            return
        if self.rowsHead.node.row == row:
            self.rowsHead = self.rowsHead.next
            return
        current = self.rowsHead
        while current.next and current.next.node.row != row:
            current = current.next
        if current.next == None:
            return
        
        current.next = current.next.next

    def removeNode(self, node):
        """Removes a node from the grid."""
        if node.up:
            node.up.down = node.down
        elif node.down:
            self.getColHead(node.col).node = node.down
        else:
            self.removeColumn(node.col)

        if node.down:
            node.down.up = node.up

        if node.left:
            node.left.right = node.right
        elif node.right:
            self.getRowHead(node.row).node = node.right
        else:
            self.removeRow(node.row)

        if node.right:
            node.right.left = node.left

        node.up = node.down = node.right = node.left = None
    
        self.updateColHeads()
        self.updateRowHeads()

    def getNodeUp(self, node: Node) -> Node:
        if not self.getColHead(node.col):
            return None
        
        cur = self.getColHead(node.col).node

        if cur == None:
            return None
        
        if node.row <= cur.row:
            return None
        
        while cur.down != None and node.row > cur.down.row:
            cur = cur.down
        
        return cur
    
    def getNodeDown(self, node: Node) -> Node:
        if not self.getColHead(node.col):
            return None

        cur = self.getColHead(node.col).node.get_down_tail()

        if cur == None:
            return None
        
        if node.row >= cur.row:
            return None

        while cur.up != None and node.row < cur.up.row:
            cur = cur.up

        return cur
    
    def getNodeLeft(self, node: Node) -> Node:
        if not self.getRowHead(node.row):
            return None

        cur = self.getRowHead(node.row).node

        if cur == None:
            return None

        if node.col <= cur.col:
            return None

        while cur.right != None and node.col > cur.right.col:
            cur = cur.right

        return cur
    
    def getNodeRight(self, node: Node) -> Node:
        if not self.getRowHead(node.row):
            return None

        cur = self.getRowHead(node.row).node.get_right_tail()

        if cur == None:
            return None

        if node.col >= cur.col:
            return None

        while cur.left != None and node.col < cur.left.col:
            cur = cur.left

        return cur

    
    def addNode(self, node):
        if self.getColHead(node.col) == None:
            new = RHNode(node)
            
            if self.colsHead == None:
                self.colsHead = new
            elif self.colsHead.node.col > node.col:
                new.next = self.colsHead
                self.colsHead = new
            else:
                current = self.colsHead
                while current.next and current.next.node.col < node.col:
                    current = current.next
                new.next = current.next
                current.next = new

        if self.getRowHead(node.row) == None:
            new = RHNode(node)

            if self.rowsHead == None:
                self.rowsHead = new
            elif self.rowsHead.node.row >= node.row:
                new.next = self.rowsHead
                self.rowsHead = new
            else:   
                current = self.rowsHead
                while current.next and current.next.node.row < node.row:
                    current = current.next
                new.next = current.next
                current.next = new
        
        if self.getNodeRight(node) != None:
            self.getNodeRight(node).left = node
        node.right = self.getNodeRight(node)
        if self.getNodeLeft(node) != None:
            self.getNodeLeft(node).right = node
        node.left = self.getNodeLeft(node)
        if self.getNodeDown(node) != None:
            self.getNodeDown(node).up = node
        node.down = self.getNodeDown(node)
        if self.getNodeUp(node) != None:
            self.getNodeUp(node).down = node
        node.up = self.getNodeUp(node)

        self.updateColHeads()
        self.updateRowHeads()

    def updateColHeads(self):
        current = self.colsHead
        while current:
            current.node = current.node.get_up_tail()
            if current.next != None and current.next.node == None:
                current = current.next.next
            else:
                current = current.next

    def updateRowHeads(self):
        current = self.rowsHead
        while current:
            current.node = current.node.get_left_tail()
            if current.next != None and current.next.node == None:
                current = current.next.next
            else:
                current = current.next

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
                if current.down and current.down.value == current.value:
                    self.merge(current, current.down)
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
                if current.up and current.up.value == current.value:
                    self.merge(current, current.up)
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
                if current.right and current.right.value == current.value:
                    self.merge(current, current.right)
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
                if current.left and current.left.value == current.value:
                    self.merge(current, current.left)
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

        self.addRandomNode()

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
    
    def updateCellsStatus(self) -> None:
        for i in range(self.size):
            for j in range(self.size):
                self.cellsStatus[i][j] = (self.getNode(i, j) != None)

    def getRandomEmptyCell(self) -> tuple:
        self.updateCellsStatus()
        empty = []

        for i in range(self.size):
            for j in range(self.size):
                if not self.cellsStatus[i][j]:
                    empty.append((i, j))

        if len(empty) == 0:
            return None
        
        x, y = empty[random.randint(0, len(empty) - 1)]
        print(f"Grid: get_random_empty_cell: Found empty cell at {x}, {y}")
        return (x, y)
    
    def addRandomNode(self) -> None:
        empty = self.getRandomEmptyCell()
        if empty == None:
            print("Grid: add_random_node: No empty cell found")
            return
        
        x, y = empty
        values = [2, 2, 2, 2, 2, 2, 2, 4, 4, 4]
        value = values[random.randint(0, 9)]
        self.addNode(Node(value, x, y))
