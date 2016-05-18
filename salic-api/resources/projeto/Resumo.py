from ..result_format import get_formated
from flask import Flask, request, make_response
from flask_restful import Resource, Api
from database.QueryHandler import QueryHandler
from ..ResourceBase import *


class Resumo(ResourceBase):
    
    def __init__(self):
        super (Resumo,self).__init__()
        
    
    def get(self, PRONAC):
        result = self.query_handler.get_resumo(PRONAC)
        if result is None:
            raise APIException('No project with PRONAC %s was found'%(PRONAC),
                                status_code = 404,
                                 message_code = 11)
        return self.result_return(result)
            