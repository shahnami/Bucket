from .collection import Collection


class PaymentCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name: str = 'Payment Collection'
        self.pages = list()
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['payment', 'banking', 'credit', 'debit']
