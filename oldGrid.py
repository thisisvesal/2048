import random
from Nodes.RHNode import RHNode
from Nodes.Node import Node

"""Obsolete"""
class Grid:
    def __init__(self, size: int, prev = None) -> None:
        self.cellsStatus = [[False for _ in range(size)] for _ in range(size)]
        if size < 2:
            print("Grid: __init__: Grid size must be at least 2")
            return
        self.size = size
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
                node = self.get(i, j)
                if node == None:
                    ans += "- "
                else:
                    ans += f"{node.value} "
            ans += "\n"

        return ans

    # Creates a row
    def _add_row(self, node: Node) -> None:
        if self._row_exists(node.row):
            print(f"Grid: _add_row: Row {node.row} already exists")
            return
        
        if self.rowsHead == None:
            self.rowsHead = RHNode(node)
            return
        
        current = self.rowsHead

        if node.row < current.node.row: # Insert new at the beginning
            new = RHNode(node)
            new.next = current
            current.prev = new
            self.rowsHead = new
            return
    
        while current.next != None and current.next.node.row < node.row:
            current = current.next

        if current == None:
            print("Grid: _add_row: None row found")
            return
        
        if current.node.row == node.row:
            print("Grid: _add_row: Row already exists but undetected")
            return
        
        new = RHNode(node)
        new.next = current.next
        if current.next != None:
            current.next.prev = new
        current.next = new
        new.prev = current

        print(f"Grid: _add_row: Added row {node.row}")

    def _remove_row(self, row: int):
        if not self._row_exists(row):
            return
        
        if self.rowsHead.node.row == row:
            self.rowsHead = self.rowsHead.next
            if self.rowsHead != None:
                self.rowsHead.prev = None
                return
            else:
                self.rowsHead = None
                return
        
        current = self.rowsHead
        while current.next != None and current.next.node.row != row:
            current = current.next
        
        if current.next == None:
            print("Grid: _remove_row: Nonexisting row undetected by _row_exists")
            return
        
        current.next = current.next.next
        if current == self.rowsHead:
            self.rowsHead = current.next
        if current.next != None:
            current.next.prev = current

        print(f"Grid: _remove_row: Removed row {row}")

    def _row_exists(self, row: int):
        current = self.rowsHead
        while current != None:
            if current.row == row:
                return True
            current = current.next
        return False
    
    def _add_col(self, node: Node) -> None:
        if self._col_exists(node.col):
            print(f"Grid: _add_col: Column {node.col} already exists")
            return
        
        if self.colsHead == None:
            self.colsHead = RHNode(node)
            return
        
        current = self.colsHead

        if node.col < current.node.col: # Insert new at the beginning
            new = RHNode(node)
            new.next = current
            current.prev = new
            self.colsHead = new
            return
        
        while current.next != None and current.next.node.col < node.col:
            current = current.next

        if current == None:
            print("Grid: _add_col: None column found")
            return
        
        if current.node.col == node.col:
            print("Grid: _add_col: Column already exists but undetected")
            return
        
        new = RHNode(node)
        new.next = current.next
        if current.next != None:
            current.next.prev = new
        current.next = new
        new.prev = current

        print(f"Grid: _add_col: Added column {node.col}")

    def _remove_col(self, col: int):
        if not self._col_exists(col):
            return
        
        if self.colsHead.node.col == col:
            self.colsHead = self.colsHead.next
            if self.colsHead != None:
                self.colsHead.prev = None
                return
            else:
                self.colsHead = None
                return
        
        current = self.colsHead
        while current.next != None and current.next.node.col != col:
            current = current.next
        
        if current.next == None:
            print("Grid: _remove_col: Nonexisting column undetected by _col_exists")
            return
        
        current.next = current.next.next
        if current == self.colsHead:
            self.colsHead = current.next
        if current.next != None:
            current.next.prev = current

        print(f"Grid: _remove_col: Removed column {col}")

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
            if current.node == None:
                print("Grid: _get_row: None head found")
                return None
            if current.node.row == row:
                return current
            current = current.next
        return None
    
    def _get_col(self, col: int) -> RHNode:
        current = self.colsHead
        while current != None:
            if current.node == None:
                print("Grid: _get_row: None head found")
                return None
            if current.node.col == col:
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
            print(f"Grid: _add_node_to_row: {node} already exists in the new location but undetected")
            return
        

        if current.right != None:
            current.right.left = node
        node.right = current.right
        node.left = current
        current.right = node

    # def _add_node_to_col(self, node: Node):
    #     if not self._col_exists(node.col):
    #         self._add_col(node)
    #         return
        
    #     head = self._get_col(node.col)

    #     # Debug
    #     if head == None:
    #         print("Grid: _add_node_to_col: None head found")
    #         return
    #     if head.node == None:
    #         print("Grid: _add_node_to_col: None column head node found")
    #         return
    #     if head.node.value == 0:
    #         print("Grid: _add_node_to_col: Head node value is 0")
    #         return
        
    #     current = head.node

    #     if node.row < current.row: # Insert new at the beginning
    #         current.up = node
    #         node.down = current
    #         node.up = None
    #         head.node = node
    #         return
        
    #     while current.down != None and current.down.row < node.row:
    #         current = current.down
        
    #     # Debug
    #     if current.row == node.row:
    #         print("Grid: _add_node_to_col: Node already exists in the new location but undetected")
    #         return
        

    #     if(current.down != None):
    #         current.down.up = node
    #     node.down = current.down
    #     node.up = current
    #     current.down = node

    def _add_node_to_col(self, node: Node):
        self._link_up(node)
        self._link_down(node)

    def _add_node_to_row(self, node: Node):
        self._link_left(node)
        self._link_right(node)

    def _link_up(self, node: Node):
        if self._get_node_up(node) == None:
            if self._get_col(node.col) == None:
                self._add_col(node)
                return
            elif self._get_col(node.col).node == None:
                self._add_col(node)
                return
            
            node.down = self._get_col(node.col).node
            node.up = None
            newHead = RHNode(node)
            self._get_col(node.col - 1).next = newHead
            newHead.next = self._get_col(node.col + 1)
            return
            
        up = self._get_node_up(node)
        up.down = node
        node.up = up

    def _link_left(self, node: Node):
        if self._get_node_left(node) == None:
            if self._get_row(node.row) == None:
                self._add_row(node)
                return
            elif self._get_row(node.row).node == None:
                self._add_row(node)
                return
            
            node.right = self._get_row(node.row).node
            node.left = None
            newHead = RHNode(node)
            self._get_row(node.row - 1).next = newHead
            newHead.next = self._get_row(node.row + 1)
            return
            
        left = self._get_node_left(node)
        left.right = node
        node.left = left

    def _link_down(self, node: Node):
        if self._get_node_down(node) == None:
            if self._get_col(node.col) == None:
                self._add_col(node)
                return
            elif self._get_col(node.col).node == None:
                self._add_col(node)
                return
            
            node.up = self._get_col(node.col).node.get_right_tail()
            node.down = None
            return
            
        down = self._get_node_down(node)
        down.up = node
        node.down = down

    def _link_right(self, node: Node):
        if self._get_node_right(node) == None:
            if self._get_row(node.row) == None:
                self._add_row(node)
                return
            elif self._get_row(node.row).node == None:
                self._add_row(node)
                return
            
            node.left = self._get_row(node.row).node.get_left_tail()
            node.right = None
            return
            
        right = self._get_node_right(node)
        right.left = node
        node.right = right

    def _get_node_up(self, node: Node) -> Node:
        if not self._col_exists(node.col):
            return None
        
        cur = self._get_col(node.col).node

        if cur == None:
            return None
        
        if node.row < cur.row:
            return None
        
        while cur.down != None and node.row > cur.down.row:
            cur = cur.down
        
        return cur
    
    def _get_node_left(self, node: Node) -> Node:
        if not self._row_exists(node.row):
            return None

        cur = self._get_row(node.row).node

        if cur == None:
            return None

        if node.col < cur.col:
            return None

        while cur.right != None and node.col > cur.right.col:
            cur = cur.right

        return cur
    
    def _get_node_down(self, node: Node) -> Node:
        if not self._col_exists(node.col):
            return None

        cur = self._get_col(node.col).node.get_bottom_tail()

        if cur == None:
            return None
        
        if node.row > cur.row:
            return None

        while cur != None and cur.row <= node.row:
            cur = cur.down

        return cur
    
    def _get_node_right(self, node: Node) -> Node:
        if not self._row_exists(node.row):
            return None

        cur = self._get_row(node.row).node.get_right_tail()

        if cur == None:
            return None

        if node.col > cur.col:
            return None

        while cur != None and cur.col <= node.col:
            cur = cur.right

        return cur


    # def _remove_node_from_row(self, node: Node) -> None:
    #     if not self._row_exists(node.row):
    #         return
        
    #     # Debug
    #     if node == None:
    #         print("Grid: _remove_node_from_row: node doesn't exist in the row")
    #         return
        
    #     head = self._get_row(node.row)
    #     # current = node
        
    #     if node.left == None and node.right != None: # Remove head node with a next
    #         head.node = node.right
    #         # if node.right != None:
    #         node.right.left = None
    #         return
        
    #     if node.left == None and node.right == None: # Remove head node without a next
    #         if node.up != None:
    #             node.up.down = node.down
    #         if node.down != None:
    #             node.down.up = node.up
    #         self._remove_row(node.row)
    #         return
        
    #     node.left.right = node.right # Remove non head node (middle or end)
    #     if node.right != None:
    #         node.right.left = node.left


    # def _remove_node_from_col(self, node: Node) -> None:
    #     if not self._col_exists(node.col):
    #         return
        
    #     # Debug
    #     if node == None:
    #         print("Grid: _remove_node_from_col: node doesn't exist in the column")
    #         return
        
    #     head = self._get_col(node.col)

    #     # node = node
        
    #     if node.up == None and node.down != None:
    #         head.node = node.down
    #         node.down.up = None
    #         return

    #     if node.up == None and node.down == None:
    #         if node.left != None:
    #             node.left.right = node.right
    #         if node.right != None:
    #             node.right.left = node.left
    #         self._remove_col(node.col)
    #         return
        
    #     node.up.down = node.down
    #     if node.down != None:
    #         node.down.up = node.up

    def _remove_node_from_col(self, node: Node) -> None:
        if node.up != None:
            node.up.down = node.down
        else:
            self._get_col(node.col).node = node.down

        if node.down != None:
            node.down.up = node.up
        # else set the column tail to node.up

    def _remove_node_from_row(self, node: Node) -> None:
        if node.left != None:
            node.left.right = node.right
        else:
            self._get_row(node.row).node = node.right

        if node.right != None:
            node.right.left = node.left
        # else set the row tail to node.left

    


    def add_node(self, node: Node) -> None:
        self._add_node_to_row(node)
        self._add_node_to_col(node)

        print(f"Grid: add_node: Added {node}")

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
        
        x, y = empty[random.randint(0, len(empty) - 1)]
        print(f"Grid: get_random_empty_cell: Found empty cell at {x}, {y}")
        return (x, y)
    
    # TODO should this be private?
    def _add_random_node(self) -> None:
        empty = self.get_random_empty_cell()
        if empty == None:
            print("Grid: add_random_node: No empty cell found")
            return
        
        x, y = empty
        values = [2, 2, 2, 2, 2, 2, 2, 4, 4, 4]
        value = values[random.randint(0, 9)]
        self.add_node(Node(value, x, y))
    
    def _has_won(self) -> bool:
        head = self.rowsHead
        while head != None:
            current = head.node
            while current != None:
                if current.value == 2048:
                    return True
                current = current.right
            head = head.next
        return False
    
    def _can_merge_in_row(self) -> bool:
        head = self.rowsHead
        while head != None:
            current = head.node
            while current != None:
                if current.next == None:
                    break
                if current.value == current.next.value:
                    return True
                current = current.right
            head = head.next
        return False
    
    def _can_merge_in_col(self) -> bool:
        head = self.colsHead
        while head != None:
            current = head.node
            while current != None:
                if current.down == None:
                    break
                if current.value == current.down.value:
                    return True
                current = current.down
            head = head.next
        return False
    
    def _can_merge(self) -> bool:
        return self._can_merge_in_col() or self._can_merge_in_row()

    
    def get_game_status(self):
        if self._has_won():
            return "won"
        if(self.get_random_empty_cell() != None or self._can_merge()):
            return "play"
        return "lost"
    
    def _move_up(self) -> None:
        head = self.colsHead
        while(head != None and head.node != None):
            current = head.node
            print(f"Grid: _move_up: head: {current}")
            
            # self._remove_node_from_row(current)
            # current.row = 0
            # head.row = 0
            # self._add_node_to_row(current)
            self._move_node_to(current, 0, current.col)

            # public static void MoveTileToCol(Tile tile, int newCol) {
            #     RemoveTileFromCol(tile);
            #     tile.col = newCol;
            #     LinkVertical(tile);
            # }

            while(current != None):
                # if (current.down != None and current.value == current.down.value):
                #     self._merge(current, current.down)
                print(f"Grid: _move_up: current: {current}")

                if current.down == None:
                    break

                # d = current.down
                # self._remove_node_from_row(current.down)
                # current.down.row = current.row + 1
                # self._add_node_to_row(current.down)
                self._move_node_to(current.down, current.row + 1, current.col)
                current = current.down

            head = head.next

    def _move_left(self) -> None:
        head = self.rowsHead
        while head != None:
            current = head.node
            print(f"Grid: _move_left: head: {current}")
            
            # self.remove_node(current)
            # current.col = 0
            # head.col = 0
            # self.add_node(current)
            self._move_node_to(current, current.row, 0)

            while current != None:
                # if current.right and current.value == current.right.value:
                #     self._merge(current, current.right)
                print(f"Grid: _move_left: current: {current}")

                if current.right == None:
                    break

                # r = current.right
                self.remove_node(current.right)
                current.right.col = current.col + 1
                self.add_node(current.right)
                # self._move_node_to(current.right, current.row, current.col + 1)
                current = current.right

            head = head.next

    def _move_down(self) -> None:
        head = self.colsHead

        if head == None:
            print("Grid: _move_down: cols head is None")
        
        while head != None:
            current = head.node.get_bottom_tail()
            print(f"Grid: _move_down: tail: {current}")

            # self._remove_node_from_row(current)
            # current.row = self.size - 1
            # self._add_node_to_row(current)
            self._move_node_to(current, self.size - 1, current.col)

            while current != None:
                # if current.up and current.value == current.up.value:
                #     self._merge(current, current.up)
                print(f"Grid: _move_down: current: {current}")

                if current.up == None:
                    break

                # TODO there's something up with this part
                # u = current.up
                self._remove_node_from_row(current.up)
                current.up.row = current.row - 1
                self._add_node_to_row(current.up)
                # self._move_node_to(current.up, current.row - 1, current.col)
                current = current.up

            head = head.next

    def _move_right(self) -> None:
        head = self.rowsHead
        if head == None:
            print("Grid: _move_right: rows head is None")
        while head != None:
            current = head.node.get_right_tail()
            print(f"Grid: _move_right: tail: {current}")
            
            # self._remove_node_from_col(current)
            # current.col = self.size - 1
            # self._add_node_to_col(current)
            self._move_node_to(current, current.row, self.size - 1)

            while current != None:
                # if current.left and current.value == current.left.value:
                #     self._merge(current, current.left)
                print(f"Grid: _move_right: current: {current}")

                if current.left == None:
                    break

                # l = current.left
                self._remove_node_from_col(current.left)
                current.left.col = current.col - 1
                self._add_node_to_col(current.left)
                # self._move_node_to(current.left, current.left.row, current.col - 1)
                current = current.left
                
            head = head.next

    def _merge(self, one: Node, other: Node) -> None:
        one.value += other.value
        self.score += one.value
        self.remove_node(other)

    def move(self, direction: str) -> None:
        if direction == "up" or direction == "w":
            self._move_up()
        elif direction == "left" or direction == "a":
            self._move_left()
        elif direction == "down" or direction == "s":
            self._move_down()
        elif direction == "right" or direction == "d":
            self._move_right()
        else:
            # Debug
            print(f"Grid: move: Invalid direction: {direction}")
            return
        
        # self._add_random_node()

    def _move_node_to_row(self, node: Node, row: int):
        # if node == None:
        #     return
        # if node.row == row:
        #     return
        
        # # if node == self.rowsHead.node:
        # #     self.rowsHead.node = node
        # # if node == self.colsHead.node:
        # #     self.colsHead.node = node
        
        self._remove_node_from_row(node)
        node.row = row
        self._add_node_to_row(node)

    def _move_node_to_col(self, node: Node, col: int):
        # if node == None:
        #     return
        # if node.col == col:
        #     return
        
        # # if node == self.rowsHead.node:
        # #     self.rowsHead.node = node
        # # if node == self.colsHead.node:
        # #     self.colsHead.node = node

        self._remove_node_from_col(node)
        node.col = col
        self._add_node_to_col(node)

    def _move_node_to(self, node: Node, row: int, col:int):
        if(node.row == row):
            self._move_node_to_col(node, col)
        elif(node.col == col):
            self._move_node_to_row(node, row)


    """Unused methods from the new grid class"""
    # def removeEmptyColumns(self):
    #     """Removes all empty columns."""
    #     current = self.colsHead
    #     prev = None
    #     while current:
    #         if current.node is None: 
    #             if prev:
    #                 prev.next = current.next
    #             else:
    #                 self.colsHead = current.next 
    #         else:
    #             prev = current 
    #         current = current.next 

    # def removeEmptyRows(self):
    #     """Removes all empty rows."""
    #     current = self.rowsHead
    #     prev = None
    #     while current:
    #         if current.node is None:
    #             if prev:
    #                 prev.next = current.next
    #             else:
    #                 self.rowsHead = current.next
    #         else:
    #             prev = current
    #         current = current.next


    """Unused method from Node"""
    # def isOrphaned(self):
    #     if self.up and not self.up.down == self:
    #         return True
    #     if self.down and not self.down.up == self:
    #         return True
    #     if self.left and not self.left.right == self:
    #         return True
    #     if self.right and not self.right.left == self:
    #         return True
        
    #     return False