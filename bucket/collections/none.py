from .collection import Collection


class NoneCollection(Collection):
    """ 
        Misc Collection class

        These are mostly sites which return page not found, or redirect to other domains other than themselves. 
        There are a few sites which ‘reset connection’ when we try and access them (status code -1) suggesting 
        while the port is open they may be expecting non-web based traffic and therefore can’t be scanned as part of the application assessment.

        The redirect sites, page not found, etc. are worth checking to ensure for example that legacy application code 
        is not present or other directory paths aren’t easily enumerable and accessible.
    """

    def __init__(self):
        Collection.__init__(self)
        self.name = 'None Collection'
        self.check = {'domain': False, 'content': True, 'status': True}
        self.keywords = ['exception-thrown', 'unhandled-status-code', '404-page-not-found',
                         '4xx-client-response', '5xx-server-response', '3xx-redirect-response', 'out-of-scope', 'error-connecting']
        self.set_weight()
