from .collection import Collection


class SocialCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.pages = list()
        self.check = {'domain': True, 'element': True}
        self.keywords = ['facebook', 'twitter',
                         'linkedin', 'reddit', 'instagram']
