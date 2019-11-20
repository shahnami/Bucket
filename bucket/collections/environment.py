from .collection import Collection


class EnvironmentCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name: str = 'Environment Collection'
        self.pages = list()
        self.check = {'domain': True, 'element': False, 'status': False}
        self.keywords = ['api', 'uat', 'dev', 'sit', 'test', 'prod', 'staging']
