class Exporter:
    """ Abstract Exporter Class """

    def __init__(self, *, output: str = './report.out'):
        self.output = output

    def export(self, *, pages: list = [], collections: list = []):
        if pages and not collections:
            self.export_pages(pages)
        elif collections and not pages:
            self.export_collections(collections)
        else:
            raise NotImplementedError(
                "Export functionality for both collections and pages simultaniously has not been implemented yet.")

    def export_pages(self, pages: list):
        raise NotImplementedError(
            "Define the export_pages function within your custom export class.")

    def export_collections(self, collections: list):
        raise NotImplementedError(
            "Define the export_collections function within your custom export class.")
