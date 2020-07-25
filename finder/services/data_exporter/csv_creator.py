from typing import List
from django.contrib.staticfiles.storage import staticfiles_storage
from finder.services.data_exporter.abstract_creator import AbstractCreator
import csv


class CsvCreator(AbstractCreator):

    def generate_report(self, data: List[dict], file_path: str) -> str:
        """
        Generates a CSV report for the provided data
        """
        file_path_with_extension = f'{file_path}.csv'
        full_file_path = staticfiles_storage.path(file_path_with_extension)

        try:
            csv_columns = data[0].keys()
        except IndexError:
            raise Exception("Can't generate a report for an empty list.")
        with open(full_file_path, mode='w') as data_file:
            writer = csv.DictWriter(data_file, fieldnames=csv_columns)
            writer.writeheader()
            for item in data:
                writer.writerow(item)
        return staticfiles_storage.url(file_path_with_extension)
