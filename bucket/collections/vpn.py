from .collection import Collection


class VPNCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.pages = list()
        self.check = {'domain': True, 'element': True}
        self.keywords = ['vpn', 'ssl']
