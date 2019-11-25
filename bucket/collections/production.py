from .collection import Collection


class ProductionCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name = 'Production Collection'
        self.pages = list()
        self.check = {'domain': True, 'content': False, 'status': False}
        self.keywords = ['prod', 'production']
        self.multiplier = 1
