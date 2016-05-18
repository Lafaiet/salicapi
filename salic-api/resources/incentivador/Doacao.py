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
         
        if request.args.get('limit') is not None:
            limit = int(request.args.get('limit'))
        else:
            limit = LIMIT_PAGING
            
        if request.args.get('offset') is not None:
            offset = int(request.args.get('offset'))
        else:
            offset = OFFSET_PAGING
        
        try:        
            results, n_records = self.query_handler.get_doacoes(cgccpf, limit, offset)
        except Exception as e:
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.result_return(result, status_code = 503)   
         
        if n_records == 0:
            result = {'message' : 'No donations was found for cgccpf %s'%(cgccpf),
                                 'message_code' : 11}
            
            return self.result_return(result, status_code = 404)
        
        headers = {'X-Total-Count' : n_records}
        return self.result_return(results, headers)
