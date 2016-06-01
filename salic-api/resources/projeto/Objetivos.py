from ..ResourceBase import *

class Objetivos(ResourceBase):
    
    def __init__(self):
        super (Objetivos,self).__init__()
        
    
    def get(self, PRONAC):
        result = self.query_handler.get_objetivos(PRONAC)
        if result is None:
            result =  { 'message' : 'No project with PRONAC %s was found'%(PRONAC),
                        'message_code' : 11
                        }
            return self.render(result, status_code = 404)
        
        return self.render(result)
            