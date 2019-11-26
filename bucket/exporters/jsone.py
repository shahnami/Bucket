import json
from .exporter import Exporter


class JSONExporter(Exporter):
    """ JSON Exporter Class """

    def export(self, collections):
        print(f"[-] Exporting to: {self.output_path}")
        with open(self.output_path, 'w') as output:
            output.writelines(json.dumps(
                [x.__dict__() for x in collections], indent=4, sort_keys=True))
