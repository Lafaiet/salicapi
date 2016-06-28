
import sys
sys.path.append('../../')
from ..ResourceBase import *
from models import PreProjetoModelObject
from ..serialization import listify_queryset
from ..sanitization import sanitize


class PreProjetoList(ResourceBase):

     def __init__(self):
        super (PreProjetoList,self).__init__()

     def get(self):

        headers = {}

        if request.args.get('limit') is not None:
            limit = int(request.args.get('limit'))

            if limit > LIMIT_PAGING:
                results = {'message' : 'Max limit paging exceeded',
                        'message_code' : 7
                    }
                return self.render(results, status_code = 405)

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
            results, n_records = PreProjetoModelObject().all(limit, offset, id, nome,
                             data_inicio, data_termino, extra_fields = True)
            Log.debug('Database call was successful')

        except Exception as e:
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        if n_records == 0:
            results = {'message' : 'No pre project was found with your criteria',
                        'message_code' : 11
                        }
            return self.render(results, status_code = 404)

        else :
            headers = {'X-Total-Count' : n_records}

        data = listify_queryset(results)

        for preprojeto in data:

            "Sanitizing text values"
            preprojeto['acessibilidade'] = sanitize(preprojeto['acessibilidade'])
            preprojeto['objetivos'] = sanitize(preprojeto['objetivos'])
            preprojeto['justificativa'] = sanitize(preprojeto['justificativa'])
            preprojeto['etapa'] = sanitize(preprojeto['etapa'])
            preprojeto['ficha_tecnica'] = sanitize(preprojeto['ficha_tecnica'])
            preprojeto['impacto_ambiental'] = sanitize(preprojeto['impacto_ambiental'])
            preprojeto['especificacao_tecnica'] = sanitize(preprojeto['especificacao_tecnica'])
            preprojeto['estrategia_execucao'] = sanitize(preprojeto['estrategia_execucao'])
            preprojeto['democratizacao'] =  sanitize(preprojeto["democratizacao"])

            preprojeto['sinopse'] = sanitize(preprojeto["sinopse"], truncated = False)
            preprojeto['resumo'] = sanitize(preprojeto["resumo"], truncated = False)

        return self.render(data, headers)
