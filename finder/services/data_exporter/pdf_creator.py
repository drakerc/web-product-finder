from finder.services.data_exporter.abstract_creator import AbstractCreator


class PdfCreator(AbstractCreator):

    def generate_report(self, data: list, file_path: str) -> str:
        raise Exception("PDFs are currently not supported")
