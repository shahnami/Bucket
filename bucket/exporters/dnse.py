import csv
from .exporter import Exporter
from ..collections import Collection


class DNSExporter(Exporter):
    """ DNS Exporter Class """

    def export(self, pages, collections):
        print(f"[-] Exporting to: {self.output_path}")

        with open(self.output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Domain', 'TXT-records', 'Technology'])

            for page in pages:
                winner = Collection.get_highest_score(page=page, collections=collections)
                if winner:
                    writer.writerow([page.domain, ', '.join([str(txt) for txt in page.dns_records['txt']]), ", ".join([matched for matched in winner.pages[page.domain]['matched']])])

