from .collection import Collection


class ProductionCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name = 'Production Collection'
        self.pages = dict()
        self.check = {'domain': True, 'content': False, 'status': False}
        self.keywords = ['prod', 'production']
        self.weight = 1
