from .collection import Collection


class InputCollection(Collection):
    """ Collection class """

    def __init__(self):
        Collection.__init__(self)
        self.name = 'Input Collection'
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['input', 'form']
        self.set_weight()
