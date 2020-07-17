from .collection import Collection


class LoginCollection(Collection):
    """ Login Collection class 

        Sites which contain common login keywords.
    """

    def __init__(self):
        Collection.__init__(self)
        self.name = 'Login Collection'
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['logon', 'signup', 'signin', 'login',
                         'register', 'auth', 'passw', 'username', 'email']
        self.set_weight()
