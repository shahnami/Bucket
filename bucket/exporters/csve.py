import csv
from .exporter import Exporter
from ..collections import Collection


class CSVExporter(Exporter):
    """ CSV Exporter Class """

    def export(self, pages, collections):
        print(f"[-] Exporting to: {self.output_path}")

        with open(self.output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Domain', 'A-records', 'Server', 'Title', 'Status',
                             'Redirected To', 'Bucket', 'Matched On', 'Valid SSL', 'Related Pages'])

            for page in pages:
                winner = Collection.get_highest_score(
                    page=page, collections=collections)
                if winner:
                    # Handle AWS slightly differently due to IP matching rather than strings
                    if(winner.name == "AWS Collection"):
                        writer.writerow([page.domain, ", ".join([str(ip) for ip in page.ip]), page.header, page.title, page.status,
                                         page.redirect['location'], winner.name, ", ".join(winner.get_match_for(partial_page=winner.pages[page.domain])), page.ssl['valid'], ", ".join([rel.domain for rel in page.related_pages])])
                    else:
                        writer.writerow([page.domain, ", ".join([str(ip) for ip in page.ip]), page.header, page.title, page.status, page.redirect['location'],
                                         winner.name, ", ".join([matched for matched in winner.pages[page.domain]['matched'] if matched in winner.keywords]), page.ssl['valid'], ", ".join([rel.domain for rel in page.related_pages])])
                else:
                    writer.writerow([page.domain, ", ".join([str(ip) for ip in page.ip]), page.header, page.title,
                                     page.status, page.redirect['location'], "NOMATCH-DEBUG", "-", page.ssl['valid'], ", ".join([rel.domain for rel in page.related_pages])])
