from enum import Enum


class Relations(Enum):
    good = 1
    neutral = 0
    bad = -1


print(Relations(1).name)  # > 'good'