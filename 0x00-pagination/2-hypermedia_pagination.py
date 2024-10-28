#!/usr/bin/env python3

import csv
from typing import List
index_range = __import__('0-simple_helper_function').index_range


class Server:
    """
    Server class for paginating a dataset of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        # Initializes the Server instance and sets dataset to None for lazy
        # loading.
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
        Loads and caches the dataset from the specified CSV file if it hasn't been loaded yet.

        Returns:
            List[List]: A list of records from the dataset, excluding the header.
        """
        # Check if the dataset is already loaded; load it from the file if not.
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip the header row

        return self.__dataset

    @staticmethod
    def assert_positive_integer_type(value: int) -> None:
        """
        Asserts that a given value is a positive integer.

        Args:
            value (int): The value to check.

        Raises:
            AssertionError: If the value is not a positive integer.
        """
        # Ensure the input value is a positive integer.
        assert isinstance(
            value, int) and value > 0, "Value must be a positive integer."

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieves a page of data from the dataset based on page number and page size.

        Args:
            page (int): The page number, must be a positive integer.
            page_size (int): The number of items per page, must be a positive integer.

        Returns:
            List[List]: A list of records for the specified page, or an empty list if out of range.
        """
        # Validate that page and page_size are positive integers.
        self.assert_positive_integer_type(page)
        self.assert_positive_integer_type(page_size)

        # Get start and end indices for the desired page.
        dataset = self.dataset()
        start, end = index_range(page, page_size)

        # Retrieve data slice; handle IndexError by returning an empty list if
        # out of range.
        try:
            data = dataset[start:end]
        except IndexError:
            data = []
        return data

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """
        Provides paginated data with hypermedia-style metadata, such as page number, total pages,
        previous and next page numbers.

        Args:
            page (int): The page number, must be a positive integer.
            page_size (int): The number of items per page, must be a positive integer.

        Returns:
            dict: A dictionary containing paginated data and additional metadata.
        """
        # Calculate the total number of pages.
        total_pages = len(self.dataset()) // page_size + 1

        # Get the data for the requested page.
        data = self.get_page(page, page_size)

        # Build metadata including page size, total pages, data, previous and
        # next pages.
        info = {
            "page": page,
            "page_size": page_size if page_size <= len(data) else len(data),
            "total_pages": total_pages,
            "data": data,
            "prev_page": page - 1 if page > 1 else None,
            "next_page": page + 1 if page + 1 <= total_pages else None
        }
        return info
