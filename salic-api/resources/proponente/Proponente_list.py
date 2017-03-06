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


class ProponenteList(ResourceBase):

    sort_fields = ['total_captado']

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

        self.proponentes_links = []

        for proponente_id in args['proponentes_ids']:
            proponente_id = encrypt(proponente_id)
            
            links = {}
            links['projetos'] = app.config['API_ROOT_URL']+'projetos/?proponente_id=%s'%proponente_id
            links['self'] = app.config['API_ROOT_URL']+'proponentes/%s'%proponente_id
            
            self.proponentes_links.append(links)


    def __init__(self):
        self.tipos_pessoa = {'1' : 'fisica', '2' : 'juridica'}
        super (ProponenteList,self).__init__()


        self.links = {
                    "self" : app.config['API_ROOT_URL']+'proponentes/',
        }

        def hal_builder(data, args = {}):
            
            total = args['total']
            count = len(data)

            hal_data = {'_links' : self.links, 'total' : total, 'count' : count}
            
            for index in range(len(data)):
                proponente = data[index]

                proponente['_links'] = self.proponentes_links[index]

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
        sort_field = None
        sort_order = None

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

        if request.args.get('proponente_id') is not None:
            proponente_id = request.args.get('proponente_id')
            cgccpf = decrypt(proponente_id)


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
            results, n_records = ProponenteModelObject().all(limit, offset, nome,
              cgccpf, municipio, UF, tipo_pessoa, sort_field, sort_order)
        except Exception as e:
            api_error = APIError('DatadabaseError')
            Log.error( '%s : '%(api_error.internal_message) + str(e) )
            return self.render(api_error.to_dict(), status_code = api_error.status_code)

        if n_records == 0 or len(results) == 0:
            api_error = APIError('ResourceNotFound')
            return self.render(api_error.to_dict(), status_code = api_error.status_code)


        print 'n_records : ' + str(n_records)
        data = listify_queryset(results)
        proponentes_ids = []

        for proponente in data:
            "Getting rid of blanks"
            proponente["cgccpf"]  = remove_blanks(str(proponente["cgccpf"]))
            proponentes_ids.append(proponente["cgccpf"])

        if cgccpf is not None:
            data = self.get_unique(cgccpf, data)
            proponentes_ids = [cgccpf]

        self.build_links(args = {'limit' : limit, 'offset' : offset, 'proponentes_ids' : proponentes_ids, 'last_offset' : n_records-1})

        for projeto_index in range(len(data)):
            data[projeto_index]['cgccpf'] = cgccpf_mask(data[projeto_index]['cgccpf'])

        headers = {'X-Total-Count' : n_records}
        return self.render(data, headers)
