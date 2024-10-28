#!/usr/bin/env python3
"""
Defines the Server class to paginate a dataset of popular baby names.
"""

import csv
import math
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculates start and end indices for pagination based on the page number and page size.

    Args:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start and end indices.
    """
    start, end = 0, 0
    for i in range(page):
        start = end
        end += page_size

    return (start, end)


class Server:
    """
    Server class to paginate a dataset of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
        Loads and caches the dataset from a CSV file if not already loaded.

        Returns:
            List[List]: The loaded dataset excluding the header row.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Exclude header row

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieves a specific page of the dataset.

        Args:
            page (int): The page number, must be a positive integer.
            page_size (int): The number of records per page, must be a positive integer.

        Returns:
            List[List]: A list of lists containing the records for the specified page,
                        or an empty list if the indices are out of range.
        """
        assert isinstance(
            page, int) and page > 0, "Page number must be a positive integer."
        assert isinstance(
            page_size, int) and page_size > 0, "Page size must be a positive integer."

        dataset = self.dataset()
        start, end = index_range(page, page_size)
        return dataset[start:end] if start < len(dataset) else []
