from ..result_format import get_formated, to_json
from flask_restful import Api
from database.QueryHandler import QueryHandler
from flask import Response
from ..ResourceBase import *

class Projeto(ResourceBase):
    
    def __init__(self):
        super (Projeto,self).__init__()
        
    
    def get(self, PRONAC):   
        
        try:
            int(PRONAC)
        except:
            result = {'message' : 'PRONAC must be an integer',
                      'message_code' : 10
                      }
            return self.result_return(result, status_code = 405)
        
        extra_fields = False
         
        if request.args.get('extra_fields') == 'true':
            extra_fields = True
        
        try:
            Log.debug('Starting database call')
            result = self.query_handler.get_by_PRONAC(PRONAC, extra_fields)
            Log.debug('Database call was successful')
        except Exception as e:
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.result_return(result, status_code = 503)
        
        if result is None:
             result = {'message' : 'No project with PRONAC %s'%(PRONAC),
                        'message_code' : 11
                        }
             return self.result_return(result, status_code = 404)
            
        
        return self.result_return(result)
