from .collection import Collection


class InputCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.pages = list()
        self.check = {'domain': True, 'element': True, }
        self.keywords = ['input', 'form']
