from ..page import Page
from ..collections import Collection


class Exporter:
    """ Abstract Exporter Class """

    def __init__(self, *, output_path: str = './report.out'):
        self.output_path = output_path

    def export(self, *, pages: [Page] = list(), collections: [Collection] = list()):
        raise NotImplementedError(
            f"The export functionality has not been implemented for {self.__class__.__name__}.")
