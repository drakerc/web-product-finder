from typing import List
from finder.models import Brand
from finder.services.data_exporter.csv_creator import CsvCreator
from finder.services.data_exporter.pdf_creator import PdfCreator
from datetime import datetime


class DataExporter:

    def __init__(self):
        self._pdf_creator = PdfCreator()
        self._csv_creator = CsvCreator()

    # TODO: I think it's a bit too tightly coupled to be a service. Needs a method that is more
    #  universal than this
    def export_brand_regexes(self, data: Brand, file_path=None, format_type='pdf') -> str:
        """
        Generates a report with regexes of a selected brand
        :param data: Brand model instance
        :param file_path: Where the report should be stored without extension, e.g. 'reports/test'
        :param format_type: Type of generated report. Currently only 'csv' is supported
        :return:
        """
        if not file_path:
            current_datetime_str = datetime.now().strftime("%Y-%m-%d-%H%M%S")
            file_path = f'reports/{current_datetime_str}_{data.name}_report'
        report_data = self._prepare_brand_regexes_report_data(data)

        if format_type == 'csv':
            return self._csv_creator.generate_report(report_data, file_path)
        if format_type == 'pdf':
            # TODO: not supported, but I don't think it needs to be supported
            return self._pdf_creator.generate_report(report_data, file_path)
        raise Exception("Unknown format type.")

    def _prepare_brand_regexes_report_data(self, data: Brand) -> List[dict]:
        """
        Creates a list of dicts with the regex data
        :param data: Brand model instance
        :return: List of dicts, e.g. [
            {'regex': '^(?=.*Fanta).*', 'created_at': 2020-07-25 11:24:13.393137+00:00}
        ]
        """
        return_data = []
        for i in data.regexes.all():
            return_data.append({
                'regex': i.rule_text,
                'created_at': i.created_at
            })
        return return_data
