from flask import Flask
from flask import request
import sys
sys.path.append('../../')
from config import LIMIT_PAGING, OFFSET_PAGING
from database.QueryHandler import QueryHandler
from ..ResourceBase import *

import pymssql, json


class Doacao(ResourceBase):
    
     def __init__(self):
        super (Doacao,self).__init__()
        
    
     def get(self, cgccpf):
        
        try:        
            results = self.query_handler.get_doacoes(cgccpf = cgccpf)
        except Exception as e:
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)   
         
        if len(results) == 0:
            result = {'message' : 'No funding info was found with your criteria',
                                 'message_code' : 11}
            
            return self.render(result, status_code = 404)
        
        return self.render(results)
