from .collection import Collection


class EnvironmentCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.pages = list()
        self.check = {'domain': True, 'element': False}
        self.keywords = ['api', 'uat', 'dev', 'sit', 'test', 'prod', 'staging']
