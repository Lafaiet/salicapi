from flask import Flask
from flask import request
import sys
sys.path.append('../../')
from models import DoacaoModelObject
from ..ResourceBase import *
from ..serialization import listify_queryset
from ..security import decrypt
from ..format_utils import remove_blanks, cgccpf_mask


import pymssql, json


class Doacao(ResourceBase):

     def __init__(self):
        super (Doacao,self).__init__()


     def get(self, url_id):

        cgccpf = decrypt(url_id)

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

        for interessado in data:
            interessado["cgccpf"] = remove_blanks(interessado['cgccpf'])
            interessado["cgccpf"] = cgccpf_mask(interessado["cgccpf"])

        return self.render(data)
