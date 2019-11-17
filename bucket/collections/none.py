from .collection import Collection


class NoneCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.pages = list()
        self.check = {'domain': False, 'element': True}
        self.keywords = ['none']
