class History:
    def __init__(self, size: int):
        self.size = size
        self.count = 0
        self.top = None
        self.bottom = None

    def __repr__(self):
        ans = ""
        cur = self.top
        while cur:
            ans += str(cur) + "\n"
            cur = cur.prev

        return ans

    def push(self, item) -> None:
        self.count += 1
        if self.top == None:
            self.top = item
            self.bottom = item
            return
        
        if self.count > self.size:
            self.bottom = self.bottom.next
            self.bottom.prev = None
            self.count -= 1
        
        item.prev = self.top
        self.top.next = item
        self.top = item

    def pop(self):
        if self.top == None:
            return None
        
        self.count -= 1
        item = self.top
        self.top = self.top.prev

        if self.top:
            self.top.next = None
        else:
            self.bottom = None

        return item
    
    def clear(self):
        self.top = None
        self.bottom = None
        self.count = 0