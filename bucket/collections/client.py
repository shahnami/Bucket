from .collection import Collection


class ClientCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name: str = 'Client Collection'
        self.pages = list()
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['input', 'form', 'contact', 'logon', 'signup', 'signin', 'login',
                         'register', 'auth', 'passw', 'username', 'email']
