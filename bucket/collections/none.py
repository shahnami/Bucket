from .collection import Collection


class NoneCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name = 'None Collection'
        self.pages = list()
        self.check = {'domain': False, 'content': True, 'status': True}
        self.keywords = ['exception-thrown', 'unhandled-status-code', '404-page-not-found',
                         '4xx-client-response', '5xx-server-response', '3xx-redirect-response', 'out-of-scope', 'error-connecting']
        self.multiplier = 9
