from flask import Flask
from flask import request
import sys
sys.path.append('../../')
from models import ProponenteModelObject
from ..ResourceBase import *
from ..APIError import APIError
from ..serialization import listify_queryset
from ..format_utils import remove_blanks, cgccpf_mask
from ..security import encrypt, decrypt


import pymssql, json


class Proponente(ResourceBase):

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

        self.projetos_links = []

        for proponente_id in args['proponentes_ids']:
            url_id = encrypt(proponente_id)
            link = app.config['API_ROOT_URL']+'projetos/?url_id=%s'%url_id
            self.projetos_links.append(link)


    def __init__(self):
        self.tipos_pessoa = {'1' : 'fisica', '2' : 'juridica'}
        super (Proponente,self).__init__()


        self.links = {
                    "self" : app.config['API_ROOT_URL']+'proponentes/',
                    "prev" : app.config['API_ROOT_URL']+'proponentes/',
                    "next" : app.config['API_ROOT_URL']+'proponentes/',
        }

        def hal_builder(data, args = {}):
            
            hal_data = {'_links' : self.links}
            
            for index in range(len(data)):
                fornecedor = data[index]

                self_link = app.config['API_ROOT_URL']+'proponentes/'
                projetos_links = self.projetos_links[index]

                fornecedor['_links'] = {}
                fornecedor['_links']['self'] = self_link
                fornecedor['_links']['projetos'] = projetos_links

            hal_data['_embedded'] = {'proponentes' : data}
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
        url_id = None

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

        if request.args.get('url_id') is not None:
            url_id = request.args.get('url_id')
            cgccpf = decrypt(url_id)

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
        proponentes_ids = []

        for proponente in data:
            "Getting rid of blanks"
            proponente["cgccpf"]  = remove_blanks(str(proponente["cgccpf"]))
            proponentes_ids.append(proponente["cgccpf"])

        if cgccpf is not None:
            data = self.get_unique(cgccpf, data)

        self.build_links(args = {'limit' : limit, 'offset' : offset, 'proponentes_ids' : proponentes_ids})

        for projeto_index in range(len(data)):
            data[projeto_index]['cgccpf'] = cgccpf_mask(data[projeto_index]['cgccpf'])

        headers = {'X-Total-Count' : n_records}
        return self.render(data, headers)
