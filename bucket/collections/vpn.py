from .collection import Collection


class VPNCollection(Collection):
    """ 
        Remote Collection class

        Sites which suggest they are remote access solutions such as Cisco VPN endpoints and Citrix.
    """

    def __init__(self):
        self.name = 'VPN Collection'
        self.pages = dict()
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['cscoe', 'netscaler', 'citrix gateway']
        self.weight = 105
