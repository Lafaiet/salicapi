from flask import Flask
from flask import request
import sys
sys.path.append('../../')
from config import LIMIT_PAGING, OFFSET_PAGING
from ..ResourceBase import *
from models import IncentivadorModelObject
from ..serialization import listify_queryset

import pymssql, json


class Incentivador(ResourceBase):

     def __init__(self):
        self.tipos_pessoa = {'1' : 'fisica', '2' : 'juridica'}
        super (Incentivador,self).__init__()


     def get(self):

        if request.args.get('limit') is not None:
            limit = int(request.args.get('limit'))
        else:
            limit = LIMIT_PAGING

        if request.args.get('offset') is not None:
            offset = int(request.args.get('offset'))
        else:
            offset = OFFSET_PAGING

        nome = None
        cgccpf = None
        municipio = None
        UF = None
        tipo_pessoa = None

        if request.args.get('nome') is not None:
            nome = request.args.get('nome')

        if request.args.get('cgccpf') is not None:
            cgccpf = request.args.get('cgccpf')

        if request.args.get('municipio') is not None:
            municipio = request.args.get('municipio')

        if request.args.get('UF') is not None:
            UF = request.args.get('UF')

        if request.args.get('tipo_pessoa') is not None:
            tipo_pessoa = request.args.get('tipo_pessoa')

        try:
            results, n_records = IncentivadorModelObject().all(limit, offset, nome, cgccpf, municipio, UF,tipo_pessoa)
        except Exception as e:
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        if n_records == 0:

            result = {'message' : 'No donator was found with your criteria',
                                 'message_code' : 11}

            return self.render(result, status_code = 404)

        headers = {'X-Total-Count' : n_records}

        data = listify_queryset(results)

        return self.render(data, headers)
