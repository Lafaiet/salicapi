
import sys
sys.path.append('../../')
from ..ResourceBase import *


class PreProjetoList(ResourceBase):
    
     def __init__(self):
        pass
    
     def get(self):
        
        headers = {}
        
        if request.args.get('limit') is not None:
            limit = int(request.args.get('limit'))
            
            if limit > LIMIT_PAGING:
                results = {'message' : 'Max limit paging exceeded',
                        'message_code' : 7
                    }
                return self.result_return(results, status_code = 405)
                
        else:
            limit = LIMIT_PAGING
            
        if request.args.get('offset') is not None:
            offset = int(request.args.get('offset'))
        else:
            offset = OFFSET_PAGING
        
        nome = None
        id = None
        data_inicio = None
        data_termino = None
        extra_fields = False
        
        if request.args.get('limit') is not None:
            limit = int(request.args.get('limit'))
         
        if request.args.get('offset') is not None:
            offset = int(request.args.get('offset'))       
        
        if request.args.get('nome') is not None:
            nome = request.args.get('nome')  

        if request.args.get('id') is not None:
            id = int(request.args.get('id')) 
        
        if request.args.get('data_inicio') is not None:
            data_inicio = request.args.get('data_inicio')
        
        if request.args.get('data_termino') is not None:
            data_termino = request.args.get('data_termino')    
        
        if request.args.get('extra_fields') == 'true':
            extra_fields = True
            
        #return_fields = request.values.getlist('fields')
        #print return_fields
                 
        try:
            Log.debug('Starting database call')
            results, n_records = self.query_handler.get_preprojeto_list(limit, offset, id, nome,
                             data_inicio, data_termino, extra_fields)
            Log.debug('Database call was successful')
        
        except Exception as e:
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.result_return(result, status_code = 503)
        
        if n_records == 0:
            results = {'message' : 'No pre project was found with your criteria',
                        'message_code' : 11
                        }
            return self.result_return(results, status_code = 404)
        
        else : 
            headers = {'X-Total-Count' : n_records}
            
        return self.result_return(results, headers)
