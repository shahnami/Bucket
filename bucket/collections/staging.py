from .collection import Collection


class StagingCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name = 'Staging Collection'
        self.pages = list()
        self.check = {'domain': True, 'content': False, 'status': False}
        self.keywords = ['staging', 'test', 'testing', 'uat',
                         'stage', 'dev', 'sit', 'integration', 'env']
        self.multiplier = 10
