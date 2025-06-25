from typing import Callable, List, Any


def find_index(filter_func: Callable[[Any], bool], lst: List[Any]) -> int:
    """
    Finds the index of the first element in the list that satisfies the filter function.

    :param filter_func: A function that takes an element and returns True if it matches the criteria.
    :param lst: The list to search through.
    :return: The index of the first matching element, or -1 if no match is found.
    """
    for index, item in enumerate(lst):
        if filter_func(item):
            return index
    return -1