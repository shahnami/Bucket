from .collection import Collection


class AuthCollection(Collection):
    """ 
        Basic Authentication Collection class

        Requires username/password via Basic Auth – typical of non-production assets.
        Note as testing is unauthenticated, testing of the application would not be possible 
        in these instances but common checks against the webserver and misconfigurations would.
    """

    def __init__(self):
        self.name = 'Auth Collection'
        self.pages = list()
        self.check = {'domain': False, 'content': False, 'status': True}
        self.keywords = ['401']
        self.multiplier = 10
