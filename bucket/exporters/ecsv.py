import csv
from .exporter import Exporter


class CSVExporter(Exporter):
    """ CSV Exporter Class """

    def export_pages(self, pages):
        print(f"[-] Exporting to: {self.output}")

        with open(self.output, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Domain', 'A-records', 'Server', 'Title', 'Status',
                             'Redirected To', 'Bucket', 'Matched On', 'Valid SSL'])

            for page in pages:
                winner, _ = page.get_top_matched()
                if winner:
                    # Handle AWS slightly differently due to IP matching rather than strings
                    if(winner.name == "AWS Collection"):
                        writer.writerow([page.domain, ", ".join([str(ip) for ip in page.ip]), page.header, page.title, page.status,
                                         page.redirect['location'], winner.name, ", ".join(winner.get_match_for(page=page)), page.ssl['valid']])
                    else:
                        writer.writerow([page.domain, ", ".join([str(ip) for ip in page.ip]), page.header, page.title, page.status, page.redirect['location'],
                                         winner.name, ", ".join([matched for matched in page.matched[winner] if matched in winner.keywords]), page.ssl['valid']])
                else:
                    writer.writerow([page.domain, ", ".join([str(ip) for ip in page.ip]), page.header, page.title,
                                     page.status, page.redirect['location'], "NOMATCH-DEBUG", "-", page.ssl['valid']])

    def export_collections(self, collections):
        pass
