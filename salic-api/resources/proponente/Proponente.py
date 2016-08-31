from flask import Flask
from flask import request
import sys
sys.path.append('../../')
from models import ProponenteModelObject
from ..ResourceBase import *
from ..APIError import APIError
from ..serialization import listify_queryset

import pymssql, json


class Proponente(ResourceBase):

     def __init__(self):
        self.tipos_pessoa = {'1' : 'fisica', '2' : 'juridica'}
        super (Proponente,self).__init__()


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
            results, n_records = ProponenteModelObject().all(limit, offset, nome, cgccpf, municipio, UF,tipo_pessoa)
        except Exception as e:
            api_error = APIError('DatadabaseError')
            Log.error( '%s : '%(api_error.internal_message) + str(e) )
            return self.render(api_error.to_dict(), status_code = api_error.status_code)

        if n_records == 0:
            api_error = APIError('ResourceNotFound')
            return self.render(api_error.to_dict(), status_code = api_error.status_code)


        data = listify_queryset(results)

        headers = {'X-Total-Count' : n_records}
        return self.render(data, headers)
