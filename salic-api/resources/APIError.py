

class ErrorCode():

    def __init__(self, status_code, message_code):
        self.status_code = status_code
        self.message_code = message_code


class APIError():


    error_types = {
        'DatadabaseError' : {'codes' : ErrorCode(500, 50), 'messages' : {'user' : "Internal Server error", 'internal' : "Problem when running a query"}},
        'ResourceNotFound' : {'codes' : ErrorCode(404, 40), 'messages' : {'user' : "No Resource was found with your criteria", 'internal' : "ResourceNotFound"}},
        'InvalidResourceName' : ErrorCode(400, 41),
        'InvalidInput' : ErrorCode(400, 42),
        'OutOfRangeQueryParameterValue' : ErrorCode(400, 43),
        'InvalidQueryParameterValue' : ErrorCode(400, 44),
        'UnsupportedQueryParameter' : ErrorCode(400, 45),
        'InvalidHeaderValue' :  ErrorCode(400, 46),
    }


    def __init__(self, error_type):
        error = self.error_types[error_type]
        self.status_code  = error['codes'].status_code
        self.message_code  = error['codes'].message_code
        self.user_message = error['messages']['user']
        self.internal_message = error['messages']['internal']

    def to_dict(self):
        return {
                'message_code' : self.message_code,
                'message' : self.user_message,
        }
