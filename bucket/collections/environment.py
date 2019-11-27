from .collection import Collection


class EnvironmentCollection(Collection):
    """ Collection class """

    def __init__(self):
        Collection.__init__(self)
        self.name = 'Environment Collection'
        self.check = {'domain': True, 'content': False, 'status': False}
        self.keywords = ['api', 'uat', 'dev', 'sit', 'test', 'prod', 'staging']
        self.set_weight()
