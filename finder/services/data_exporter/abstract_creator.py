import abc
from typing import List


class AbstractCreator(abc.ABC):

    @abc.abstractmethod
    def generate_report(self, data: List[dict], file_path: str) -> str:
        """
        Generates a report file based on the provided data.
        :param data: List of dictionaries where the dictionaries' key will be used as a
         title/column and the value will be a row. For example,
         [
            {'id': 1, 'title': 'pepsi'},
            {'id': 2, 'title': 'sprite'}
        ] - the report will use ID and title as titles/columns and it will create two rows of data
        :param file_path: file path of the created report, e.g. 'reports/new_report.csv'
        :return: A path to the newly generated report in the static directory,
         e.g. '/static/reports/new_report.csv'
        """
        pass
