
# Name: Jaskaran Singh Sidhu
# OSU Email: sidhuja@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 2: Bag ADT
# Description: Implements a Bag ADT using a Dynamic Array.


from dynamic_array import DynamicArray, DynamicArrayException


class Bag:
    def __init__(self, start_bag=None):
        self._da = DynamicArray()
        if start_bag:
            for value in start_bag:
                self.add(value)

    def add(self, value: object) -> None:
        self._da.append(value)

    def remove(self, value: object) -> bool:
        for i in range(self._da.length()):
            if self._da.get_at_index(i) == value:
                for j in range(i, self._da.length() - 1):
                    self._da.set_at_index(j, self._da.get_at_index(j + 1))
                self._da.remove_at_index(self._da.length() - 1)
                return True
        return False

    def count(self, value: object) -> int:
        count = 0
        for i in range(self._da.length()):
            if self._da.get_at_index(i) == value:
                count += 1
        return count

    def clear(self) -> None:
        self._da = DynamicArray()

    def equal(self, second_bag: 'Bag') -> bool:
        if self._da.length() != second_bag._da.length():
            return False

        matched = set()
        for i in range(self._da.length()):
            found_match = False
            for j in range(second_bag._da.length()):
                if j in matched:
                    continue
                if self._da.get_at_index(i) == second_bag._da.get_at_index(j):
                    matched.add(j)
                    found_match = True
                    break
            if not found_match:
                return False
        return True

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < self._da.length():
            value = self._da.get_at_index(self._index)
            self._index += 1
            return value
        else:
            raise StopIteration
