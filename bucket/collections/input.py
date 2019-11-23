from .collection import Collection


class InputCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name = 'Input Collection'
        self.pages = list()
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['input', 'form']
