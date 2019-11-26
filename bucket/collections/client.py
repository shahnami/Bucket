from .collection import Collection


class ClientCollection(Collection):
    """ 
        Interactive Collection class

        Sites which match a number of keywords such as login, username, password, etc. 
        suggesting they have authenticated areas and therefore may host data that could be classified as sensitive.
    """

    def __init__(self):
        self.name = 'Client Collection'
        self.pages = dict()
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['input', 'form', 'contact', 'logon', 'signup', 'signin', 'login',
                         'register', 'auth', 'passw', 'username', 'email', 'online-banking', 'dashboard', 'secure.']
        self.weight = 1
