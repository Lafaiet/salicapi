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


class FornecedorDetail(ResourceBase):


    def build_links(self, args = {}):

        fornecedor_id = args['fornecedor_id']

        self.links['self'] += fornecedor_id
        self.links['produtos'] = self.links['self'] + '/produtos'


    def __init__(self):
        super (FornecedorDetail, self).__init__()

        self.links = {
                    "self" : app.config['API_ROOT_URL']+'fornecedores/',
        }

        def hal_builder(data, args = {}):
            
            hal_data = data
            hal_data['_links'] = self.links
            
            return hal_data

        self.to_hal = hal_builder


    def get(self, fornecedor_id):

        cgccpf = decrypt(fornecedor_id)


        try:
            results = FornecedordorModelObject().all(limit=1, offset=0, cgccpf = cgccpf)
        except Exception as e:
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  17,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        results = listify_queryset(results)

        n_records = len(results)

        if n_records == 0 or len(results) == 0:

            result = {'message' : 'No supplier was found with your criteria',
                                 'message_code' : 11}

            return self.render(result, status_code = 404)

        headers = {}

        data = results
        fornecedor = data[0]

      
        fornecedor["cgccpf"]  = remove_blanks(fornecedor["cgccpf"])

        self.build_links(args = {'fornecedor_id' : fornecedor_id})

       
        fornecedor["cgccpf"] = cgccpf_mask(fornecedor["cgccpf"])


        return self.render(fornecedor, headers)
