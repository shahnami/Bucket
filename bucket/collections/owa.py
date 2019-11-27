from .collection import Collection


class OWACollection(Collection):
    """ 
        Microsoft OWA Collection Class

        Sites which appear as Microsoft OWA instances
    """

    def __init__(self):
        Collection.__init__(self)
        self.name = 'OWA Collection'
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['/owa/', 'Outlook Web App',
                         'Connected to Microsoft Exchange', 'OwaPage']
        self.set_weight()
