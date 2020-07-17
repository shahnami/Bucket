from .collection import Collection


class PaymentCollection(Collection):
    """ Payment Collection class 

        Sites which contain payment elements.
    """

    def __init__(self):
        Collection.__init__(self)
        self.name = 'Payment Collection'
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['payment', 'banking', 'credit', 'debit']
        self.set_weight()
