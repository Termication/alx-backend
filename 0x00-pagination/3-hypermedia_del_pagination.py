#!/usr/bin/env python3

import csv
import math
from typing import List, Dict


class Server:
    """
    Server class for handling and paginating a dataset of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        # Initializes the Server instance with placeholders for the full dataset
        # and an indexed dataset to facilitate deletion-resilient pagination.
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """
        Loads and caches the full dataset from the CSV file if it hasn't been loaded already.

        Returns:
            List[List]: The full dataset, excluding the header row.
        """
        # Load and cache the dataset from the file if not already loaded.
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip the header row

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """
        Caches the first 1000 rows of the dataset as a dictionary with integer indices 
        as keys to create an indexed, deletion-resilient dataset.

        Returns:
            Dict[int, List]: A dictionary where each key is an index and each value 
                             is a dataset row, up to 1000 rows.
        """
        # Load and cache an indexed version of the dataset if it hasn't been created.
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]  # Limit to the first 1000 rows
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Provides a deletion-resilient paginated response starting from a specific index 
        with a specified page size.

        Args:
            index (int): The starting index for pagination.
            page_size (int): The number of items per page.

        Returns:
            Dict: A dictionary with pagination details including data, 
                  starting index, page size, and the next index.
        """
        # Retrieve the indexed dataset and validate that the index is within bounds.
        dataset = self.indexed_dataset()
        data_length = len(dataset)
        assert 0 <= index < data_length, "Index out of range."
        
        # Initialize the response dictionary and prepare to collect the paginated data.
        response = {}
        data = []
        response['index'] = index  # Record the starting index
        
        # Collect `page_size` elements, accounting for any deleted indices.
        for i in range(page_size):
            while True:
                curr = dataset.get(index)
                index += 1
                # Continue to the next index if the current one is missing.
                if curr is not None:
                    break
            data.append(curr)

        # Populate the response dictionary with the collected data and metadata.
        response['data'] = data
        response['page_size'] = len(data)
        
        # Determine the next index, if it exists; otherwise set to None.
        if dataset.get(index):
            response['next_index'] = index
        else:
            response['next_index'] = None

        return response
