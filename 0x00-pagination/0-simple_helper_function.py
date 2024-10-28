#!/usr/bin/env python3
"""
task 0
"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the start and end index for a
    given page in pagination.

    Args:
        page (int): The current page number (1-based).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple with the start and
        end indices for the items on the requested page.
    """

    start, end = 0, 0
    for i in range(page):
        start = end
        end += page_size

    return (start, end)
