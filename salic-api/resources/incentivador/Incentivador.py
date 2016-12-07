from flask import Flask
from flask import request
import sys
sys.path.append('../../')
from ..ResourceBase import *
from models import IncentivadorModelObject
from ..serialization import listify_queryset
from ..format_utils import remove_blanks, cgccpf_mask
from ..security import encrypt, decrypt


import pymssql, json


class Incentivador(ResourceBase):

    def build_links(self, args = {}):

        query_args = '&'

        for arg in request.args:
            if arg!= 'limit' and arg != 'offset':
                query_args+=arg+'='+request.args[arg]+'&'

        self.links["self"] += '?limit=%d&offset=%d'%(args['limit'], args['offset'])+query_args
        self.links["next"] += '?limit=%d&offset=%d'%(args['limit'], args['offset']+args['limit'])+query_args

        if args['offset']-args['limit'] < 0:
            self.links["prev"] += '?limit=%d&offset=%d'%(args['limit'], 0)+query_args

        else:
            self.links["prev"] += '?limit=%d&offset=%d'%(args['limit'], args['offset']-args['limit'])+query_args

        self.doacoes_links = []

        for incentivador_id in args['incentivadores_ids']:
            url_id = encrypt(incentivador_id)
            link = app.config['API_ROOT_URL']+'incentivadores/%s/doacoes/'%url_id
            self.doacoes_links.append(link)

    def __init__(self):
        self.tipos_pessoa = {'1' : 'fisica', '2' : 'juridica'}
        super (Incentivador,self).__init__()

        self.links = {
                    "self" : app.config['API_ROOT_URL']+'incentivadores/',
                    "prev" : app.config['API_ROOT_URL']+'incentivadores/',
                    "next" : app.config['API_ROOT_URL']+'incentivadores/',
        }

        def hal_builder(data, args = {}):
            
            hal_data = {'_links' : self.links}
            
            for index in range(len(data)):
                incentivador = data[index]

                self_link = app.config['API_ROOT_URL']+'incentivadores/'
                doacoes_links = self.doacoes_links[index]

                incentivador['_links'] = {}
                incentivador['_links']['self'] = self_link
                incentivador['_links']['doacoes'] = doacoes_links

            hal_data['_embedded'] = {'incentivadores' : data}
            return hal_data

        self.to_hal = hal_builder


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

        if request.args.get('url_id') is not None:
            url_id = request.args.get('url_id')
            cgccpf = decrypt(url_id)

        if request.args.get('municipio') is not None:
            municipio = request.args.get('municipio')

        if request.args.get('UF') is not None:
            UF = request.args.get('UF')

        if request.args.get('tipo_pessoa') is not None:
            tipo_pessoa = request.args.get('tipo_pessoa')

        if request.args.get('PRONAC') is not None:
            PRONAC = request.args.get('PRONAC')

        try:
            results, n_records = IncentivadorModelObject().all(limit, offset, nome, cgccpf, municipio, UF,tipo_pessoa, PRONAC)

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
        incentivadores_ids = []

        for incentivador in data:
            "Getting rid of blanks"
            incentivador["cgccpf"]  = remove_blanks(str(incentivador["cgccpf"]))
            incentivadores_ids.append(incentivador['cgccpf'])

        if cgccpf is not None:
            data = self.get_unique(cgccpf, data)

        self.build_links(args = {'limit' : limit, 'offset' : offset, 'incentivadores_ids' : incentivadores_ids})

        for incentivador in data:
            incentivador["cgccpf"] = cgccpf_mask(incentivador["cgccpf"])

        return self.render(data, headers)
