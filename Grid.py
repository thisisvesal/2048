import random
from Nodes.RHNode import RHNode
from Nodes.Node import Node

class Grid:
    def __init__(self, size: int, maxTile=2048, prev=None) -> None:
        if size < 2:
            print("Grid: __init__: Grid size must be at least 2")
            return

        self.size = size
        self.maxTile = maxTile
        self.rowsHead = None
        self.colsHead = None
        self.prev = prev
        self.next = None
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
    
    def __eq__(self, other):
        if not isinstance(other, Grid):
            return False
        elif self.size != other.size:
            return False
        
        for i in range(self.size):
            for j in range(self.size):
                if self.getNode(i, j) != other.getNode(i, j):
                    return False
                
        return True
    
    def __ne__(self, other):
        return not self.__eq__(other)
            

    def moveNodeTo(self, node, row, column):
        """Moves a given node to the specified row and column"""
        # Remove the node
        self.removeNode(node)

        # Reposition
        node.row = row
        node.col = column

        # Add updated node
        self.addNode(node)

    def moveNodeToColumn(self, node, column):
        """Moves a given node to a specific column"""
        self.removeNode(node)
        node.col = column
        self.addNode(node)

    def removeColumn(self, col):
        """Removes a column from the grid"""
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
        """Removes a row from the grid"""
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
        """Removes a node from the grid"""
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

    # The following four methods are used to get the node that should be in a specific direction respective to the input node
    # So at the point where this is called, the return value is not necessarily actually next to the input node
    # But it should be position wise

    def getNodeUp(self, node: Node) -> Node:
        """Returns the node that should be above the given node"""
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
        """Returns the node that should be below the given node"""
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
        """Returns the node that should be to the left of the given node"""
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
        """Returns the node that should be to the right of the given node"""
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
        """Add a node to the grid"""
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
        """Updates the column heads"""
        current = self.colsHead
        while current:
            current.node = current.node.get_up_tail()
            if current.next != None and current.next.node == None:
                current = current.next.next
            else:
                current = current.next

    def updateRowHeads(self):
        """Update the row heads"""
        current = self.rowsHead
        while current:
            current.node = current.node.get_left_tail()
            if current.next != None and current.next.node == None:
                current = current.next.next
            else:
                current = current.next

    def getNode(self, row, column):
        """Gets a node from the grid by its position"""
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
        """Moves all nodes up in their respective columns"""
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
        """Moves all nodes down in their respective columns"""
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
        """Moves all nodes left in their respective rows"""
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
        """Moves all nodes right in their respective rows"""
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
        """Moves the grid nodes in the specified direction"""
        if direction == "up" or direction == "w":
            self.moveUp()
        elif direction == "left" or direction == "a":
            self.moveLeft()
        elif direction == "down" or direction == "s":
            self.moveDown()
        elif direction == "right" or direction == "d":
            self.moveRight()

    def merge(self, one: Node, other: Node) -> None:
        "Merges two nodes into the first one"
        one.value += other.value
        self.score += one.value
        self.removeNode(other)

    def getRowHead(self, row):
        """Returns the head node of a specific row"""
        current = self.rowsHead
        while current:
            if current.node.row == row:
                return current
            current = current.next
        return None

    def getColHead(self, column):
        """Returns the head node of a specific column"""
        current = self.colsHead
        while current:
            if current.node.col == column:
                return current
            current = current.next
        return None

    def getEmptyCells(self) -> list:
        empty = []

        for i in range(self.size):
            for j in range(self.size):
                if self.getNode(i, j) == None:
                    empty.append((i, j))

        return empty


    def getRandomEmptyCell(self) -> tuple:
        """Returns a random empty cell position"""
        empty = self.getEmptyCells()

        if len(empty) == 0:
            return None
        
        x, y = empty[random.randint(0, len(empty) - 1)]

        return (x, y)
    
    def addRandomNode(self) -> None:
        """Adds a new node with a value of 2 or 4 to a random empty cell"""
        empty = self.getRandomEmptyCell()
        if empty == None:
            return
        
        x, y = empty
        values = [2, 2, 2, 2, 2, 2, 2, 4, 4, 4] # 70% chance of getting 2, 30% chance of getting 4
        value = values[random.randint(0, 9)]
        self.addNode(Node(value, x, y))

    def canMergeInRow(self) -> bool:
        """Checks if any two nodes can be merged horizontally"""
        head = self.rowsHead
        while head != None:
            current = head.node
            while current != None and current.right != None:
                if current.value == current.right.value:
                    return True
                current = current.right
            head = head.next
        return False
    
    def canMergeInCol(self) -> bool:
        """Checks if any two nodes can be merged vertically"""
        head = self.colsHead
        while head != None:
            current = head.node
            while current != None and current.down:
                if current.value == current.down.value:
                    return True
                current = current.down
            head = head.next
        return False
    
    def canMerge(self) -> bool:
        """Checks if any two nodes can be merged"""
        return self.canMergeInCol() or self.canMergeInRow()
    
    def isGameOver(self):
        """Checks if no more moves can be made and game is over"""
        # Basically checks if there are any empty cells or if anything can be merged
        # If neither holds, game is over
        return self.getRandomEmptyCell() == None and not self.canMerge()
    
    def hasWon(self):
        """Checks if the player has won the game"""
        head = self.rowsHead
        while head:
            current = head.node
            while current:
                if current.value == self.maxTile:
                    return True
                current = current.right
            head = head.next
        return False
    

    # Minimax utils:

    def countEmptyInRow(self, row: int):
        """Counts the number of empty cells in a row"""
        return self.size - self.countRow(row)
    
    def countEmptyInCol(self, col: int):
        """Counts the number of empty cells in a column"""
        return self.size - self.countCol(col)
    
    def sumOfRow(self, row: int):
        """Returns the sum of the values in a row"""
        sum = 0
        head = self.getRowHead(row)
        if not head:
            return 0
        
        current = head.node
        while current:
            sum += current.value
            current = current.right

        return sum
    
    def sumOfCol(self, col: int):
        """Returns the sum of the values in a column"""
        sum = 0
        head = self.getColHead(col)
        if not head:
            return 0
        
        current = head.node
        while current:
            sum += current.value
            current = current.down

        return sum

    def getPresentMaxValue(self):
        maximum = -1

        head = self.rowsHead
        while head:
            current = head.node
            while current:

                if current.value > maximum:
                    maximum = current.value

                current = current.right
            head = head.next

        return maximum
    
    def getMaxInRow(self, row: int):
        maximum = -1
        head = self.getRowHead(row)
        if not head:
            return 0
        
        current = head.node
        while current:
            if current.value > maximum:
                maximum = current.value
            current = current.right

        return maximum
    
    def getRowOrderGrade(self, row: int):
        """Grades tiles' arrangement in a row"""
        grade = 0
        head = self.getRowHead(row)
        if not head:
            return 0
        
        current = head.node
        while current:
            grade += current.value
            current = current.right

        return grade

    def getUpperLeftMostEmpty(self) -> tuple:
        """Returns the position of the upper left most empty cell"""
        for i in range(self.size):
            for j in range(self.size):
                if self.getNode(i, j) == None:
                    return (i, j)
        return None
    
    def countRow(self, i: int):
        """Counts the number of nodes in a row"""
        count = 0
        current = self.getRowHead(i)
        if current == None:
            return 0
        current = current.node
        while current:
            count += 1
            current = current.right
        return count
    
    def countCol(self, j: int):
        """Counts the number of nodes in a column"""
        count = 0
        current = self.getColHead(j)
        if current == None:
            return 0
        current = current.node
        while current:
            count += 1
            current = current.down
        return count

    

