from .collection import Collection


class ProductionCollection(Collection):
    """ Collection class """

    def __init__(self):
        Collection.__init__(self)
        self.name = 'Production Collection'
        self.check = {'domain': True, 'content': False, 'status': False}
        self.keywords = ['prod', 'production']
        self.set_weight()
