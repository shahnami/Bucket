from .collection import Collection


class LoginCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name = 'Login Collection'
        self.pages = dict()
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['logon', 'signup', 'signin', 'login',
                         'register', 'auth', 'passw', 'username', 'email']
        self.weight = 1
