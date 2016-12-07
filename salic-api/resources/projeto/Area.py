from flask_restful import Api
from flask import Response
from ..ResourceBase import *
from models import AreaModelObject
from ..serialization import listify_queryset



class Area(ResourceBase):

    def __init__(self):
        super (Area,self).__init__()

        def hal_builder(data, args = {}):
            
            hal_data = {'_links' : {'self' : app.config['API_ROOT_URL']+'projetos/areas/'}}
            
            for area in data:

                link = app.config['API_ROOT_URL']+'projetos/?area=%s'%area['codigo']  
                area['_links'] = {'self' : link}

            
            hal_data['_embedded'] = {'areas' : data}

            return hal_data

        self.to_hal = hal_builder




    def get(self):

        try:
            result = AreaModelObject().all()
        except Exception as e:
            Log.error(str())
            result = {'message' : 'internal error',
                                 'message_code' : 13,
                      }

            return self.render(result, status_code = 503)

        result = listify_queryset(result)

        return self.render(result)
