from flask import Flask
from flask import request
import sys
sys.path.append('../../')
from config import LIMIT_PAGING, OFFSET_PAGING
from models import DoacaoModelObject
from ..ResourceBase import *
from ..serialization import listify_queryset

import pymssql, json


class Doacao(ResourceBase):

     def __init__(self):
        super (Doacao,self).__init__()


     def get(self, cgccpf):

        try:
            results = DoacaoModelObject().all(cgccpf = cgccpf)
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

        data = listify_queryset(results)

        return self.render(data)
