from .collection import Collection


class SocialCollection(Collection):
    """ Collection class """

    def __init__(self):
        Collection.__init__(self)
        self.name = 'Social Collection'
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['facebook', 'twitter',
                         'linkedin', 'reddit', 'instagram']
        self.set_weight()
