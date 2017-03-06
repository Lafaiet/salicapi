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


class IncentivadorList(ResourceBase):

    sort_fields = ['total_doado']

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
        


        self.doacoes_links = []

        for incentivador_id in args['incentivadores_ids']:
            links = {}
            incentivador_id_enc = encrypt(incentivador_id)

            links['self'] = app.config['API_ROOT_URL'] + 'incentivadores/%s'%incentivador_id_enc
            links['doacoes'] = app.config['API_ROOT_URL']+'incentivadores/%s/doacoes/'%incentivador_id_enc

            self.doacoes_links.append(links)

    def __init__(self):
        self.tipos_pessoa = {'1' : 'fisica', '2' : 'juridica'}
        super (IncentivadorList,self).__init__()

        self.links = {
                    "self" : app.config['API_ROOT_URL']+'incentivadores/',
        }

        def hal_builder(data, args = {}):
            
            total = args['total']
            count = len(data)

            hal_data = {'_links' : self.links, 'total' : total, 'count' : count}
            
            for index in range(len(data)):
                incentivador = data[index]

                doacoes_links = self.doacoes_links[index]

                incentivador['_links'] = doacoes_links
                

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
        sort_field = None
        sort_order = None

        if request.args.get('nome') is not None:
            nome = request.args.get('nome')

        if request.args.get('cgccpf') is not None:
            cgccpf = request.args.get('cgccpf')

        if request.args.get('incentivador_id') is not None:
            incentivador_id = request.args.get('incentivador_id')
            cgccpf = decrypt(incentivador_id)

        if request.args.get('municipio') is not None:
            municipio = request.args.get('municipio')

        if request.args.get('UF') is not None:
            UF = request.args.get('UF')

        if request.args.get('tipo_pessoa') is not None:
            tipo_pessoa = request.args.get('tipo_pessoa')

        if request.args.get('PRONAC') is not None:
            PRONAC = request.args.get('PRONAC')

        if request.args.get('sort') is not None:
            sorting = request.args.get('sort').split(':')

            if len(sorting) == 2:
                sort_field = sorting[0]
                sort_order = sorting[1]
            elif len(sorting) == 1:
                sort_field = sorting[0]
                sort_order = 'asc'

            if sort_field not in self.sort_fields:
                Log.error('sorting field error: '+str(sort_field))
                result = {'message' : 'field error: "%s"'%sort_field,
                      'message_code' :  10,
                      }
                return self.render(result, status_code = 405)

        try:
            results, n_records = IncentivadorModelObject().all(limit, offset, nome, cgccpf,
                                                                municipio, UF,tipo_pessoa, PRONAC,
                                                                sort_field, sort_order)

        except Exception as e:
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        if n_records == 0 or len(results) == 0:

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
            incentivadores_ids = [cgccpf]

        self.build_links(args = {'limit' : limit, 'offset' : offset, 'incentivadores_ids' : incentivadores_ids, 'last_offset' : n_records-1})

        for incentivador in data:
            incentivador["cgccpf"] = cgccpf_mask(incentivador["cgccpf"])

        return self.render(data, headers)
