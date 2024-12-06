from History import History
from TestNode import TestNode

history = History(5)
history.push(TestNode(1))
history.push(TestNode(2))

print("Before:")
print(history)

print("pop ", end=" ")
print(history.pop())


print("After:")
print(history)

print("pop ", end=" ")
print(history.pop())


print("After:")
print(history)

print("pop ", end=" ")
print(history.pop())

print("After:")
print(history)