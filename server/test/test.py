
from typing import List, TypeVar

T = TypeVar("T")

def first(container: List[T]) -> T:
    return container[0]
  
if __name__ == "__main__":
    list_one: List[str] = ["a", "b", "c"]
    print(first(list_one))
    
    list_two: List[int] = [1, 2, 3]
    print(first(list_two))