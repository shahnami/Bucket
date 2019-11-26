from .collection import Collection


class InputCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name = 'Input Collection'
        self.pages = dict()
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['input', 'form']
        self.weight = 1
