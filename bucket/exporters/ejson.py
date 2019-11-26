import json
from .exporter import Exporter


class JSONExporter(Exporter):
    """ JSON Exporter Class """

    def export_pages(self, pages):
        pass

    def export_collections(self, collections):
        print(f"[-] Exporting to: {self.output}")
        with open(self.output, 'w') as output:
            output.writelines(json.dumps(
                [x.__dict__() for x in collections], indent=4, sort_keys=True))
