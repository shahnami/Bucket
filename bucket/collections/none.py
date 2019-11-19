from .collection import Collection


class NoneCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name: str = 'None Collection'
        self.pages = list()
        self.check = {'domain': False, 'element': True}
        self.keywords = ['none', '404-page-not-found',
                         '4xx-client-error', '5xx-server-error']
