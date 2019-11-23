from .collection import Collection


class AuthCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name = 'Auth Collection'
        self.pages = list()
        self.check = {'domain': False, 'content': False, 'status': True}
        self.keywords = ['401']
        self.multiplier = 10
