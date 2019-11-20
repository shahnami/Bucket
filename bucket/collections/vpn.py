from .collection import Collection


class VPNCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name: str = 'VPN Collection'
        self.pages = list()
        self.check = {'domain': True, 'element': True, 'status': False}
        self.keywords = ['vpn', 'ssl']
