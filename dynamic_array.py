
# Name: Jaskaran Singh Sidhu
# OSU Email: sidhuja@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 2: Dynamic Array and Bag ADT
# Description: Dynamic Array Implementation,This file implements a Dynamic Array class using a static array as its internal storage.The class provides various functionalities similar to Python lists, including resizing,appending, inserting, removing, and additional features such as slice, map, filter, reduce, and chunking the array into subarrays of non-descending order. 

#Each method is designed to adhere to specific time complexities, and severalmethods implement error handling to ensure robustness. This file also containsthe find_mode function to identify the most frequently occurring element(s) in a sorted dynamic array.


from static_array import StaticArray


class DynamicArrayException(Exception):
    pass


class DynamicArray:
    def __init__(self, arr=None):
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)
        
        if arr:
            for item in arr:
                self.append(item)

    def resize(self, new_capacity: int) -> None:
        if new_capacity <= 0 or new_capacity < self._size:
            return
        
        new_data = StaticArray(new_capacity)
        for i in range(self._size):
            new_data.set_at_index(i, self._data.get_at_index(i))
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value: object) -> None:
        if self._size == self._capacity:
            self.resize(self._capacity * 2)
        self._data.set_at_index(self._size, value)
        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        if index < 0 or index > self._size:
            raise DynamicArrayException("Invalid index")
        
        if self._size == self._capacity:
            self.resize(self._capacity * 2)
        
        for i in range(self._size, index, -1):
            self._data.set_at_index(i, self._data.get_at_index(i - 1))
        
        self._data.set_at_index(index, value)
        self._size += 1

    def remove_at_index(self, index: int) -> None:
        if index < 0 or index >= self._size:
            raise DynamicArrayException("Invalid index")
        
        if self._size < self._capacity // 4 and self._capacity > 10:
            new_capacity = max(self._size * 2, 10)
            self.resize(new_capacity)
        
        for i in range(index, self._size - 1):
            self._data.set_at_index(i, self._data.get_at_index(i + 1))
        
        self._size -= 1
        self._data.set_at_index(self._size, None)

    def slice(self, start_index: int, size: int) -> 'DynamicArray':
        if start_index < 0 or start_index >= self._size or size < 0 or start_index + size > self._size:
            raise DynamicArrayException("Invalid slice parameters")
        
        result = DynamicArray()
        for i in range(size):
            result.append(self.get_at_index(start_index + i))
        return result

    def map(self, map_func) -> 'DynamicArray':
        result = DynamicArray()
        for i in range(self._size):
            result.append(map_func(self._data.get_at_index(i)))
        return result

    def filter(self, filter_func) -> 'DynamicArray':
        result = DynamicArray()
        for i in range(self._size):
            if filter_func(self._data.get_at_index(i)):
                result.append(self._data.get_at_index(i))
        return result

    def reduce(self, reduce_func, initializer=None) -> object:
        if self._size == 0:
            return initializer
        
        result = initializer if initializer is not None else self._data.get_at_index(0)
        start_index = 0 if initializer is not None else 1
        
        for i in range(start_index, self._size):
            result = reduce_func(result, self._data.get_at_index(i))
        return result

    def length(self) -> int:
        return self._size

    def get_at_index(self, index: int) -> object:
        if index < 0 or index >= self._size:
            raise DynamicArrayException("Invalid index")
        return self._data.get_at_index(index)


def chunk(arr: DynamicArray) -> DynamicArray:
    chunked_array = DynamicArray()
    if arr.length() == 0:
        return chunked_array
    
    current_chunk = DynamicArray()
    current_chunk.append(arr.get_at_index(0))
    
    for i in range(1, arr.length()):
        if arr.get_at_index(i) >= arr.get_at_index(i - 1):
            current_chunk.append(arr.get_at_index(i))
        else:
            chunked_array.append(current_chunk)
            current_chunk = DynamicArray()
            current_chunk.append(arr.get_at_index(i))
    
    if current_chunk.length() > 0:
        chunked_array.append(current_chunk)
    
    return chunked_array


def find_mode(arr: DynamicArray) -> tuple:
    if arr.length() == 0:
        return DynamicArray(), 0
    
    mode_array = DynamicArray()
    max_count = 1
    current_count = 1
    current_value = arr.get_at_index(0)
    mode_array.append(current_value)
    
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
    
    if current_count > max_count:
        return DynamicArray([current_value]), current_count
    elif current_count == max_count:
        mode_array.append(current_value)
    
    return mode_array, max_count
