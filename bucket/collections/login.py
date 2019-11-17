from .collection import Collection


class LoginCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.pages = list()
        self.check = {'domain': True, 'element': True}
        self.keywords = ['logon', 'signup', 'signin', 'login',
                         'register', 'auth', 'passw', 'username', 'email']
