from .collection import Collection


class StagingCollection(Collection):
    """ 
        Non-Production Collection class

        Sites which match common keywords such as uat and sit, suggesting they are non-production.
    """

    def __init__(self):
        self.name = 'Staging Collection'
        self.pages = list()
        self.check = {'domain': True, 'content': False, 'status': False}
        self.keywords = ['staging', 'test', 'testing', 'uat',
                         'stage', 'dev', 'sit', 'integration', 'env']
        self.multiplier = 11
