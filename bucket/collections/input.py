from .collection import Collection


class InputCollection(Collection):
    """ Input Collection class 

        Sites which contain elements commonly used for search, registration or login functionalities.
    """

    def __init__(self):
        Collection.__init__(self)
        self.name = 'Input Collection'
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['input', 'form']
        self.set_weight()
