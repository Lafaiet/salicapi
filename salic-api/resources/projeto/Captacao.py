from ..result_format import get_formated, to_json
from flask_restful import Api
from flask import Response
from ..ResourceBase import *
from models import CaptacaoModelObject
from ..serialization import listify_queryset

class Captacao(ResourceBase):

    def __init__(self):
       super (Captacao,self).__init__()


    def get(self, PRONAC):

        try:
            results = CaptacaoModelObject().all(PRONAC = PRONAC)
        except Exception as e:
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)


        if len(results) == 0:
            results = {'message' : 'No funding info was found with your criteria',
                        'message_code' : 11
                        }
            return self.render(results, status_code = 404)

        data = listify_queryset(results)

        return self.render(data)
