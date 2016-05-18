






class APIError():

    def __init__(self, message, status_code, message_code, payload=None):
        Exception.__init__(self)
        self.status_code = status_code
        self.message_code  = message_code
        self.message = message
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['code'] = self.message_code
        rv['more_info'] = 'http://api.novosalic/doc'
        return rv