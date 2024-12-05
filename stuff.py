class Grid:
    def __init__(self, size: int, prev=None) -> None:
        if size < 2:
            print("Grid: __init__: Grid size must be at least 2")
            return
        
        self.cellsStatus = [[False for _ in range(size)] for _ in range(size)]
        self.size = size
        self.rowsHead = None  # RHNode for rows
        self.colsHead = None  # RHNode for columns

        self.prev = prev
        self.next = None
        self.score = 0

    def addNode(self, row: int, col: int) -> Node:
        """Adds a new node to the grid."""
        if self.cellsStatus[row][col]:
            return None  # Node already exists
        new_node = Node(row, col)
        self.cellsStatus[row][col] = True
        self._link_to_headers(new_node)
        return new_node

    def removeNode(self, row: int, col: int) -> None:
        """Removes a node from the grid."""
        if not self.cellsStatus[row][col]:
            return  # Node does not exist
        node = self.getNode(row, col)
        if not node:
            return
        # Unlink the node from neighbors
        if node.up:
            node.up.down = node.down
        if node.down:
            node.down.up = node.up
        if node.left:
            node.left.right = node.right
        if node.right:
            node.right.left = node.left

        self.cellsStatus[row][col] = False
        self._clean_headers()

    def getNode(self, row: int, col: int) -> Node:
        """Gets the node at a specific position."""
        cur = self.rowsHead
        while cur:
            if cur.node.row == row:
                node = cur.node
                while node:
                    if node.col == col:
                        return node
                    node = node.right
            cur = cur.next
        return None

    def moveNodeTo(self, node: Node, row: int, col: int) -> None:
        """Moves a node to a new row and column."""
        self.removeNode(node.row, node.col)
        node.row = row
        node.col = col
        self.addNode(row, col)

    def move_up(self) -> None:
        """Moves all nodes up."""
        cur_col = self.colsHead
        while cur_col:
            cur_node = cur_col.node
            row_index = 0
            while cur_node:
                self.moveNodeTo(cur_node, row_index, cur_node.col)
                cur_node = cur_node.down
                row_index += 1
            cur_col = cur_col.next
        self._clean_headers()

    def move_down(self) -> None:
        """Moves all nodes down."""
        cur_col = self.colsHead
        while cur_col:
            cur_node = cur_col.node.get_down_tail()
            row_index = self.size - 1
            while cur_node:
                self.moveNodeTo(cur_node, row_index, cur_node.col)
                cur_node = cur_node.up
                row_index -= 1
            cur_col = cur_col.next
        self._clean_headers()

    def move_left(self) -> None:
        """Moves all nodes to the left."""
        cur_row = self.rowsHead
        while cur_row:
            cur_node = cur_row.node
            col_index = 0
            while cur_node:
                self.moveNodeTo(cur_node, cur_node.row, col_index)
                cur_node = cur_node.right
                col_index += 1
            cur_row = cur_row.next
        self._clean_headers()

    def move_right(self) -> None:
        """Moves all nodes to the right."""
        cur_row = self.rowsHead
        while cur_row:
            cur_node = cur_row.node.get_right_tail()
            col_index = self.size - 1
            while cur_node:
                self.moveNodeTo(cur_node, cur_node.row, col_index)
                cur_node = cur_node.left
                col_index -= 1
            cur_row = cur_row.next
        self._clean_headers()

    def _link_to_headers(self, node: Node) -> None:
        """Links a node to the appropriate row and column headers."""
        # Link to row header
        # (Create the header if it doesn't exist and add the node)

        # Link to column header
        # (Similar logic as above)

        pass  # To be



