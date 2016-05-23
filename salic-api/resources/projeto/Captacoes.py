from ..result_format import get_formated, to_json
from flask_restful import Api
from database.QueryHandler import QueryHandler
from flask import Response
from ..ResourceBase import *

class Captacoes(ResourceBase):
    
    def __init__(self):
       super (Captacoes,self).__init__()
        
    
    def get(self, PRONAC):
        
        try:
            results = self.query_handler.get_captacoes(PRONAC)
        except Exception as e:
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.result_return(result, status_code = 503)
       
     
        if len(results) == 0:
            results = {'message' : 'No funding info was found with your criteria',
                        'message_code' : 11
                        }
            return self.result_return(results, status_code = 404)
            
        return self.result_return(results)
    
