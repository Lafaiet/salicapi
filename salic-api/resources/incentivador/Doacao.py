from flask import Flask
from flask import request
import sys
sys.path.append('../../')
from models import DoacaoModelObject
from ..ResourceBase import *
from ..serialization import listify_queryset
from ..security import decrypt
from ..format_utils import remove_blanks, cgccpf_mask
from ..security import encrypt 


import pymssql, json


class Doacao(ResourceBase):

     def build_links(self, args = {}):

        self.links = {'self' : ''}

        incentivador_id = args['incentivador_id']

        self.links["self"] = app.config['API_ROOT_URL'] + 'incentivadores/%s/doacoes/'%incentivador_id

        self.doacoes_links = []

        for doacao in args['doacoes']:
                doacao_links = {}
                doacao_links['projeto'] = app.config['API_ROOT_URL'] + 'projetos/%s'%doacao['PRONAC']
                incentivador_id = encrypt(doacao['cgccpf'])
                doacao_links['incentivador'] = app.config['API_ROOT_URL'] + 'incentivadores/%s'%incentivador_id

                self.doacoes_links.append(doacao_links)

     def __init__(self):
        super (Doacao,self).__init__()

        def hal_builder(data, args = {}):

            hal_data = {'_links' : ''}
            
            hal_data['_links']  = self.links

            hal_data['_embedded'] = {'doacoes' : ''}

            for index in range(len(data)):
                doacao = data[index]
                doacao['_links'] = self.doacoes_links[index]
                
            hal_data['_embedded']['doacoes'] = data

            return hal_data

        self.to_hal = hal_builder

     def get(self, incentivador_id):

        cgccpf = decrypt(incentivador_id)
        print cgccpf

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

        for doacao in data:
            doacao["cgccpf"] = remove_blanks(doacao['cgccpf'])

        data = self.get_unique(cgccpf, data)

        self.build_links(args = {'incentivador_id' : incentivador_id, 'doacoes' : data})

        for doacao in data:
            doacao["cgccpf"] = cgccpf_mask(doacao["cgccpf"])

        return self.render(data)
