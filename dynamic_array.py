# Name: Jaskaran Singh Sidhu
# OSU Email: sidhuja@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 2: Dynamic Array and Bag ADT
# Description: Implements a Dynamic Array with additional operations including resizing, slicing, mapping, filtering, and reducing.

from static_array import StaticArray

class DynamicArrayException(Exception):
    """Custom exception to be used by DynamicArray."""
    pass

class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize the dynamic array.
        This uses a static array for storage, which resizes as needed.
        """
        self._size = 0  # keeps track of the number of elements
        self._capacity = 4  # initial capacity
        self._data = StaticArray(self._capacity)

        # If an array was provided, add its elements to the dynamic array
        if start_array:
            for value in start_array:
                self.append(value)

    def __str__(self):
        """
        Returns a string representation of the array for debugging purposes.
        """
        output = "DYN_ARR Size/Cap: {}/{} [" \
                 .format(self._size, self._capacity)
        output += ', '.join([str(self._data[i]) for i in range(self._size)])
        return output + ']'

    def is_empty(self) -> bool:
        """
        Returns True if the array has no elements, otherwise False.
        """
        return self._size == 0

    def length(self) -> int:
        """
        Returns the number of elements currently stored in the array.
        """
        return self._size

    def get_at_index(self, index: int) -> object:
        """
        Returns the element at the specified index.
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException("Index out of bounds")
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Sets the value at the specified index.
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException("Index out of bounds")
        self._data[index] = value

    def get_capacity(self) -> int:
        """
        Returns the current capacity of the array.
        """
        return self._capacity

    def resize(self, new_capacity: int) -> None:
        """
        Changes the capacity of the array to new_capacity if it’s valid.
        """
        if new_capacity <= 0 or new_capacity < self._size:
            return  # Exit if new capacity is invalid

        new_data = StaticArray(new_capacity)
        for i in range(self._size):
            new_data[i] = self._data[i]

        self._data = new_data
        self._capacity = new_capacity

    def append(self, value: object) -> None:
        """
        Adds a new element to the end of the array.
        If the array is full, doubles its capacity first.
        """
        if self._size == self._capacity:
            self.resize(2 * self._capacity)

        self._data[self._size] = value
        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserts a value at the given index, shifting elements as necessary.
        """
        if index < 0 or index > self._size:
            raise DynamicArrayException("Index out of bounds")

        if self._size == self._capacity:
            self.resize(2 * self._capacity)

        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]

        self._data[index] = value
        self._size += 1

    def remove_at_index(self, index: int) -> None:
        """
        Removes an element at the specified index, adjusting capacity if needed.
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException("Index out of bounds")

        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]

        self._data[self._size - 1] = None
        self._size -= 1

        # Adjust capacity based on conditions, respecting minimum capacity of 10 or half-size
        if self._size < self._capacity // 4 and self._capacity > 10:
            new_capacity = max(10, self._capacity // 2)
            self.resize(new_capacity)

    def slice(self, start_index: int, size: int) -> 'DynamicArray':
        """
        Returns a new DynamicArray with elements from start_index of given size.
        """
        if start_index < 0 or size < 0 or start_index + size > self._size:
            raise DynamicArrayException("Invalid slice parameters")

        sliced_array = DynamicArray()
        for i in range(start_index, start_index + size):
            sliced_array.append(self._data[i])

        return sliced_array

    def map(self, map_func) -> 'DynamicArray':
        """
        Applies map_func to each element and returns a new DynamicArray of results.
        """
        mapped_array = DynamicArray()
        for i in range(self._size):
            mapped_array.append(map_func(self._data[i]))

        return mapped_array

    def filter(self, filter_func) -> 'DynamicArray':
        """
        Returns a new DynamicArray with elements that pass filter_func.
        """
        filtered_array = DynamicArray()
        for i in range(self._size):
            if filter_func(self._data[i]):
                filtered_array.append(self._data[i])

        return filtered_array

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Applies reduce_func to elements, accumulating result with initializer.
        """
        if self.is_empty():
            return initializer

        result = initializer if initializer is not None else self._data[0]
        start_index = 0 if initializer is not None else 1

        for i in range(start_index, self._size):
            result = reduce_func(result, self._data[i])

        return result


# Standalone functions chunk and find_mode as specified
def chunk(arr: DynamicArray) -> DynamicArray:
    """
    Breaks array into subarrays of non-descending values.
    """
    result = DynamicArray()
    if arr.is_empty():
        return result

    current_chunk = DynamicArray()
    current_chunk.append(arr.get_at_index(0))

    for i in range(1, arr.length()):
        if arr.get_at_index(i) >= arr.get_at_index(i - 1):
            current_chunk.append(arr.get_at_index(i))
        else:
            result.append(current_chunk)
            current_chunk = DynamicArray()
            current_chunk.append(arr.get_at_index(i))

    result.append(current_chunk)
    return result

def find_mode(arr: DynamicArray) -> tuple:
    """
    Finds mode(s) in sorted DynamicArray.
    """
    if arr.is_empty():
        return DynamicArray(), 0

    mode_array = DynamicArray()
    current_count = 1
    max_count = 1
    current_value = arr.get_at_index(0)

    for i in range(1, arr.length()):
        if arr.get_at_index(i) == current_value:
            current_count += 1
        else:
            if current_count > max_count:
                max_count = current_count
                mode_array = DynamicArray()
                mode_array.append(current_value)
            elif current_count == max_count:
                mode_array.append(current_value)
            current_value = arr.get_at_index(i)
            current_count = 1

    # Final check for last element group
    if current_count > max_count:
        mode_array = DynamicArray()
        mode_array.append(current_value)
        max_count = current_count
    elif current_count == max_count:
        mode_array.append(current_value)

    return mode_array, max_count
