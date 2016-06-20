from ..result_format import get_formated, to_json
from flask_restful import Api
from flask import Response
from ..ResourceBase import *
from models import SegmentoModelObject

class Segmento(ResourceBase):

    def __init__(self):
        super (Segmento,self).__init__()


    def get(self):

        try:
            result = SegmentoModelObject().all()
        except:
            result =  { 'message' : 'internal error',
                        'message_code' : 13
                        }
            return self.render(result, status_code = 503)

        data = []

        for item in result:
            data.append(item[0])

        return self.render(data)
