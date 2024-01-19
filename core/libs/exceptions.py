class FyleError(Exception):
    """
    Base exception class.
    """
    status_code = 400

    def __init__(self, status_code, message):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        res = dict()
        res['message'] = self.message
        res['status_code'] = self.status_code
        return res


# There should be more exceptions that specify the error code and message.
# for e.g
# class NotFoundError(FyleError):
#     status_code = 404
#     message = 'Not Found'
    
# class NotAuthenticated(FyleError):
#     status_code = 400
#     message = 'Bad Request'
    
