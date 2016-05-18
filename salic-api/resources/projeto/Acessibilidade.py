from ..ResourceBase import *

class Acessibilidade(ResourceBase):
    
    def __init__(self):
        pass
    
    def get(self, PRONAC):
        result = self.query_handler.get_acessibilidade(PRONAC)
        if result is None:
            result = APIerror('No project with PRONAC %s was found'%(PRONAC),
                                status_code = 404,
                                 message_code = 11)
        return self.result_return(result)
            