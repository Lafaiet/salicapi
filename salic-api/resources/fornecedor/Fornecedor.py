from flask import Flask
from flask import request
import sys
sys.path.append('../../')
from ..ResourceBase import *
from models import FornecedordorModelObject
from ..serialization import listify_queryset

import pymssql, json


class Fornecedor(ResourceBase):

     def __init__(self):
        super (Fornecedor, self).__init__()


     def get(self):

        if request.args.get('limit') is not None:
            limit = int(request.args.get('limit'))
        else:
            limit = app.config['LIMIT_PAGING']

        if request.args.get('offset') is not None:
            offset = int(request.args.get('offset'))
        else:
            offset = app.config['OFFSET_PAGING']

        nome = None
        cgccpf = None
        municipio = None
        UF = None
        tipo_pessoa = None
        PRONAC = None

        if request.args.get('nome') is not None:
            nome = request.args.get('nome')

        if request.args.get('cgccpf') is not None:
            cgccpf = request.args.get('cgccpf')

        if request.args.get('PRONAC') is not None:
            PRONAC = request.args.get('PRONAC')

        try:
            results = FornecedordorModelObject().all(cgccpf = cgccpf, PRONAC =  PRONAC, nome  = nome)
        except Exception as e:
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  17,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        results = listify_queryset(results)

        if len(results) == 0:

            result = {'message' : 'No supplier was found with your criteria',
                                 'message_code' : 11}

            return self.render(result, status_code = 404)

        headers = {'X-Total-Count' : len(results)}

        data = results

        return self.render(data, headers)
