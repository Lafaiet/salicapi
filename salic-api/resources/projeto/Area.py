from flask_restful import Api
from flask import Response
from ..ResourceBase import *
from models import AreaModelObject


class Area(ResourceBase):

    def __init__(self):
       super (Area,self).__init__()


    def get(self):

        try:
            result = AreaModelObject().all()
        except Exception as e:
            Log.error(str())
            result = {'message' : 'internal error',
                                 'message_code' : 13,
                      }

            return self.render(result, status_code = 503)

        data = []

        for item in result:
            data.append(item[0])

        return self.render(data)
