from enum import Enum, auto


class Color(int, Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


print(Color.BLUE.value)  # 3
print(Color.BLUE.name)  # BLUE

if Color.BLUE > Color.RED:
    print("Hello")


class NewColor(str, Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


if len(NewColor.GREEN.value) > len(NewColor.RED.value):
    print("Hello again")


class AnotherColor(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
