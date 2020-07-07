from .collection import Collection


class DNSCollection(Collection):
    """ 
        DNS TXT Collection Class

        Gather technologies based on TXT records.
    """

    def __init__(self):
        Collection.__init__(self)
        self.name = 'DNS Collection'
        self.check = {'domain': False, 'content': False, 'status': False}
        self.keywords = ['keybase', 'google', 'adobe',
                         'cloudflare', 'cloudhealth', 'onetrust', 'globalsign', 'ms=', 'salesforce', 'messagelabs', 'facebook', 'quovadis', 'zendesk', 'mastercard', 'outlook', 'mailjet', 'firm58', 'qualtrics', 'grassroots', 'sendgrid', 'greenhouse.io', 'wp-noop', 'dropbox', 'workplace', 'taleo', 'azure', 'worldsecuresystem']
        self.set_weight()

    def validate(self, *, page):
        entry: dict = {"page": page, "matched": list()}
        for keyword in self.keywords:
            for record in page.dns_records['txt']:
                if keyword.lower() in record.lower():
                    if 'ms=' in keyword.lower():
                        entry['matched'].append('microsoft office 365')
                    else:
                        entry['matched'].append(keyword)

                    entry['matched'] = list(set(entry['matched']))

        if entry['matched']:
            self.pages[page.domain] = entry