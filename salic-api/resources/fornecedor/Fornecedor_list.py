from flask import Flask
from flask import request
import sys
sys.path.append('../../')
from ..ResourceBase import *
from models import FornecedordorModelObject
from ..serialization import listify_queryset
from ..format_utils import remove_blanks, cgccpf_mask
from ..security import encrypt, decrypt


import pymssql, json


class FornecedorList(ResourceBase):


    def build_links(self, args = {}):

        query_args = '&'

        for arg in request.args:
            if arg!= 'limit' and arg != 'offset':
                query_args+=arg+'='+request.args[arg]+'&'

        if args['offset']-args['limit'] >= 0:
            self.links["prev"] = self.links["self"] + '?limit=%d&offset=%d'%(args['limit'], args['offset']-args['limit'])+query_args
            

        if args['offset']+args['limit'] <= args['last_offset']:
            self.links["next"] = self.links["self"] + '?limit=%d&offset=%d'%(args['limit'], args['offset']+args['limit'])+query_args
        
        self.links["first"] = self.links["self"] + '?limit=%d&offset=0'%(args['limit'])+query_args
        self.links["last"] = self.links["self"] + '?limit=%d&offset=%d'%(args['limit'], args['last_offset'])+query_args
        self.links["self"] += '?limit=%d&offset=%d'%(args['limit'], args['offset'])+query_args

        self.fornecedores_links = []

        for fornecedor_id in args['fornecedores_ids']:
            links = {}
            fornecedor_id_enc = encrypt(fornecedor_id)

            links['self'] = app.config['API_ROOT_URL'] + 'fornecedores/%s'%fornecedor_id_enc
            links['produtos'] = app.config['API_ROOT_URL']+'fornecedores/%s/produtos/'%fornecedor_id_enc

            self.fornecedores_links.append(links)


    def __init__(self):
        super (FornecedorList, self).__init__()

        self.links = {
                    "self" : app.config['API_ROOT_URL']+'fornecedores/',
        }

        def hal_builder(data, args = {}):
            total = args['total']
            count = len(data)

            hal_data = {'_links' : self.links, 'total' : total, 'count' : count}
            
            for f_index in range(len(data)):
                fornecedor = data[f_index]

                fornecedores_links = self.fornecedores_links[f_index]

                fornecedor['_links'] = fornecedores_links

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

        if request.args.get('fornecedor_id') is not None:
            fornecedor_id = request.args.get('fornecedor_id')
            cgccpf = decrypt(fornecedor_id)

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

        n_records = FornecedordorModelObject().count(cgccpf = cgccpf, PRONAC =  PRONAC, nome  = nome)
        n_records = listify_queryset(n_records)

        n_records = n_records[0]['total']

        if n_records == 0 or len(results) == 0:

            result = {'message' : 'No supplier was found with your criteria',
                                 'message_code' : 11}

            return self.render(result, status_code = 404)

        headers = {'X-Total-Count' : n_records}

        data = results
        fornecedores_ids = []

        for fornecedor in data:
            "Getting rid of blanks"
            fornecedor["cgccpf"]  = remove_blanks(str(fornecedor["cgccpf"]))
            fornecedores_ids.append(fornecedor['cgccpf'])

        if cgccpf is not None:
            data = self.get_unique(cgccpf, data)

        self.build_links(args = {'limit' : limit, 'offset' : offset, 'fornecedores_ids' : fornecedores_ids, 'last_offset' : n_records-1})

        for fornecedor in data:
            fornecedor["cgccpf"] = cgccpf_mask(fornecedor["cgccpf"])


        return self.render(data, headers)
