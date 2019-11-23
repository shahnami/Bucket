from .collection import Collection


class VPNCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name = 'VPN Collection'
        self.pages = list()
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['cscoe', 'netscaler', 'citrix gateway']
        self.multiplier = 100
