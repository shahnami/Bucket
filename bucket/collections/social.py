from .collection import Collection


class SocialCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name = 'Social Collection'
        self.pages = dict()
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['facebook', 'twitter',
                         'linkedin', 'reddit', 'instagram']
        self.weight = 1
