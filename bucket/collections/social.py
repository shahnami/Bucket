from .collection import Collection


class SocialCollection(Collection):
    """ Social Collection class 

        Sites that contain elements related to social platforms.
    """

    def __init__(self):
        Collection.__init__(self)
        self.name = 'Social Collection'
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['facebook', 'twitter',
                         'linkedin', 'reddit', 'instagram']
        self.set_weight()
