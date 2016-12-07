from flask import Flask
from flask import request
import sys
sys.path.append('../../')
from ..ResourceBase import *
from models import FornecedordorModelObject
from ..serialization import listify_queryset
from ..format_utils import remove_blanks, cgccpf_mask
from ..security import encrypt 


import pymssql, json


class Fornecedor(ResourceBase):


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

        self.produtos_links = []

        for fornecedor_id in args['fornecedores_ids']:
            url_id = encrypt(fornecedor_id)
            link = app.config['API_ROOT_URL']+'fornecedores/%s/produtos/'%url_id
            self.produtos_links.append(link)


    def __init__(self):
        super (Fornecedor, self).__init__()

        self.links = {
                    "self" : app.config['API_ROOT_URL']+'fornecedores/',
                    "prev" : app.config['API_ROOT_URL']+'fornecedores/',
                    "next" : app.config['API_ROOT_URL']+'fornecedores/',
        }

        def hal_builder(data, args = {}):
            
            hal_data = {'_links' : self.links}
            
            for f_index in range(len(data)):
                fornecedor = data[f_index]

                self_link = app.config['API_ROOT_URL']+'fornecedores/'
                produtos_links = self.produtos_links[f_index]

                fornecedor['_links'] = {}
                fornecedor['_links']['self'] = self_link
                fornecedor['_links']['produtos'] = produtos_links

            hal_data['_embedded'] = {'fornecedores' : data}
            return hal_data

        self.to_hal = hal_builder


    def get(self):

        if request.args.get('limit') is not None:
            limit = int(request.args.get('limit'))

            if limit > app.config['LIMIT_PAGING']:
                results = {'message' : 'Max limit paging exceeded',
                        'message_code' : 7
                    }
                return self.render(results, status_code = 405)

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
            results = FornecedordorModelObject().all(limit, offset, cgccpf = cgccpf, PRONAC =  PRONAC, nome  = nome)
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
        fornecedores_ids = []

        for fornecedor in data:
            "Getting rid of blanks"
            fornecedor["cgccpf"]  = remove_blanks(str(fornecedor["cgccpf"]))
            fornecedores_ids.append(fornecedor['cgccpf'])

        if cgccpf is not None:
            data = self.get_unique(cgccpf, data)

        self.build_links(args = {'limit' : limit, 'offset' : offset, 'fornecedores_ids' : fornecedores_ids})

        for fornecedor in data:
            fornecedor["cgccpf"] = cgccpf_mask(fornecedor["cgccpf"])


        return self.render(data, headers)
