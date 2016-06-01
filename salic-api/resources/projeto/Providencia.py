from ..result_format import get_formated
from flask import Flask, request, make_response
from flask_restful import  Api
from database.QueryHandler import QueryHandler
from ..ResourceBase import *



class Providencia(ResourceBase):
    
    def __init__(self):
        super (Providencia,self).__init__()
        
    
    def get(self, PRONAC):
        result = self.query_handler.get_providencia(PRONAC)
        if result is None:
            result =  { 'message' : 'No project with PRONAC %s was found'%(PRONAC),
                        'message_code' : 11
                        }
            return self.render(result, status_code = 404)
            
        return self.render(result)
            
    