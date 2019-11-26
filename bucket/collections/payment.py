from .collection import Collection


class PaymentCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name = 'Payment Collection'
        self.pages = dict()
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['payment', 'banking', 'credit', 'debit']
        self.weight = 1
