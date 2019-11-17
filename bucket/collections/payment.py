from .collection import Collection


class PaymentCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.pages = list()
        self.check = {'domain': True, 'element': True, }
        self.keywords = ['payment', 'banking']
