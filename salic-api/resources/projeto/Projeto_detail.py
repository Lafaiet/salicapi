from flask_restful import Api
from flask import Response
from ..ResourceBase import *
from models import ProjetoModelObject
from ..serialization import listify_queryset



class ProjetoDetail(ResourceBase):

    def __init__(self):
        super (ProjetoDetail,self).__init__()


    def get(self, PRONAC):

        try:
            int(PRONAC)
        except:
            result = {'message' : 'PRONAC must be an integer',
                      'message_code' : 10
                      }
            return self.render(result, status_code = 405)

        extra_fields = False

        if request.args.get('extra_fields') == 'true':
            extra_fields = True

        try:
            Log.debug('Starting database call')
            result, n_records = ProjetoModelObject().all(limit=1, offset=0, PRONAC = PRONAC, extra_fields = extra_fields)
            Log.debug('Database call was successful')
        except Exception as e:
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        if n_records == 0:
             result = {'message' : 'No project with PRONAC %s'%(PRONAC),
                        'message_code' : 11
                        }
             return self.render(result, status_code = 404)

        data = listify_queryset(result)[0]

        return self.render(data)
