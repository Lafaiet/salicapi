import sys
sys.path.append('../../')
from ..ResourceBase import *


class ProjetoList(ResourceBase):
    
     def __init__(self):
        super (ProjetoList,self).__init__()
    
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
        
        PRONAC = None
        nome = None
        proponente = None
        cgccpf = None
        area = None
        segmento = None
        UF = None
        data_inicio = None
        data_termino = None
        extra_fields = False
        
        if request.args.get('limit') is not None:
            limit = int(request.args.get('limit'))
         
        if request.args.get('offset') is not None:
            offset = int(request.args.get('offset'))   
        
        if request.args.get('PRONAC') is not None:
            PRONAC = request.args.get('PRONAC')
        
        if request.args.get('nome') is not None:
            nome = request.args.get('nome')
        
        if request.args.get('proponente') is not None:
            proponente = request.args.get('proponente')
            
        if request.args.get('cgccpf') is not None:
            cgccpf = request.args.get('cgccpf')
            
        if request.args.get('area') is not None:
            area = request.args.get('area')
            
        if request.args.get('segmento') is not None:
            segmento = request.args.get('segmento')  
        
        if request.args.get('segmento') is not None:
            segmento = request.args.get('segmento')  
            
        if request.args.get('UF') is not None:
            UF = request.args.get('UF')  
        
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
            results, n_records = self.query_handler.get_projeto_list(limit, offset, PRONAC, nome,
                              proponente, cgccpf, area, segmento,
                              UF, data_inicio, data_termino, extra_fields)
            Log.debug('Database call was successful')
        
        except Exception as e:
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.result_return(result, status_code = 503)
        
        if n_records == 0:
            results = {'message' : 'No project was found with your criteria',
                        'message_code' : 11
                        }
            return self.result_return(results, status_code = 404)
        
        else : 
            headers = {'X-Total-Count' : n_records}
            
        return self.result_return(results, headers)
