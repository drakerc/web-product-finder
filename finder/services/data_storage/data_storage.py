from dataclasses import dataclass
from typing import List
from django.conf import settings
import pandas as pd
import os


@dataclass
class Product:
    id_source: str
    name: str
    item_description: str
    category: str


class DataStorage:
    """
    Singleton-style class that imports products data from a file.
    Currently supports files with pandas gzipped dataframe.
    """

    def __init__(self, path: str, columns: list, sample_size: int = 10000):
        """
        :param path (str): Path to the file containing products
        :param columns (list): List of columns that should be imported, e.g. ['name', 'id_source']
        :param sample_size: Amount of products that will be imported
        """
        self.products_list = self.import_products(path, columns, sample_size)

    def import_products(self, path: str, columns: list, sample_size: int = 10000) -> List[Product]:
        """
        Imports products from a file depending on its extension
        # TODO: should probably support more extensions, but not really sure what kind of...
        """
        if not os.path.exists(path):
            raise Exception("Products file does not exist.")
        file_extension = os.path.splitext(path)[1][1:]
        if file_extension in ['parquet', 'pq', 'gzip']:
            return self._import_parquet(path, columns, sample_size)
        raise Exception(f"Unsupported products file extension: {file_extension}")

    def _import_parquet(self, path: str, columns: list, sample_size: int = 10000) -> List[Product]:
        """
        Imports products from a parquet-type file
        """
        dataframe = pd.read_parquet(path, columns=columns)
        products = []
        for row in dataframe[:sample_size].itertuples(index=True, name='Products'):
            products.append(
                Product(
                    id_source=row.id_source,
                    name=row.name,
                    item_description=row.item_description,
                    category=row.category
                )
            )
        return products


data_storage = DataStorage(
    settings.PRODUCTS_FILE,
    settings.PRODUCTS_FILE_COLUMNS,
    settings.PRODUCTS_FILE_SAMPLE_SIZE
)
