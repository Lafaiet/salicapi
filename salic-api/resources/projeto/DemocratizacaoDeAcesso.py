from ..result_format import get_formated
from flask import Flask, request, make_response
from flask_restful import Resource, Api
from database.QueryHandler import QueryHandler
from ..ResourceBase import *

class DemocratizacaoDeAcesso(ResourceBase):
    
    def __init__(self):
        super (DemocratizacaoDeAcesso,self).__init__()
        
    
    def get(self, PRONAC):
        result = self.query_handler.get_democratizacao_de_acesso(PRONAC)
        if result is None:
            
            result = {'message' : 'No project with PRONAC %s was found'%(PRONAC),
                                 'message_code' : 11,
                      }
            
            return self.result_return(result, status_code = 404)   
        
        return self.result_return(result)
            