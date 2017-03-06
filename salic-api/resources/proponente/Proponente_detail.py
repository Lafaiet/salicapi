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


class ProponenteDetail(ResourceBase):

    sort_fields = ['total_captado']

    def build_links(self, args = {}):

        proponente_id = args['proponente_id']

        self.links['self'] += proponente_id
        self.links['projetos'] += proponente_id

    def __init__(self):
        self.tipos_pessoa = {'1' : 'fisica', '2' : 'juridica'}
        super (ProponenteDetail,self).__init__()


        self.links = {
                    "self" : app.config['API_ROOT_URL']+'proponentes/',
                    "projetos" : app.config['API_ROOT_URL']+'projetos/?proponente_id=',
        }

        def hal_builder(data, args = {}):
            
            hal_data = data
            hal_data['_links'] = self.links
            
            return hal_data

        self.to_hal = hal_builder


    def get(self, proponente_id):
           
        cgccpf = decrypt(proponente_id)

        try:
            results, n_records = ProponenteModelObject().all(limit=1, offset=0, cgccpf=cgccpf)
        except Exception as e:
            api_error = APIError('DatadabaseError')
            Log.error( '%s : '%(api_error.internal_message) + str(e) )
            return self.render(api_error.to_dict(), status_code = api_error.status_code)

        if n_records == 0 or len(results) == 0:
            api_error = APIError('ResourceNotFound')
            return self.render(api_error.to_dict(), status_code = api_error.status_code)


        data = listify_queryset(results)
        proponente = data[0]

       
        proponente["cgccpf"]  = remove_blanks(str(proponente["cgccpf"]))

        self.build_links(args = {'proponente_id' : proponente_id })
        proponente["cgccpf"] = cgccpf_mask(proponente["cgccpf"])

        headers = {}

        return self.render(proponente, headers)
