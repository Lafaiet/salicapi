
import sys
sys.path.append('../../')
from ..ResourceBase import *
from models import PreProjetoModelObject
from ..serialization import listify_queryset
from ..sanitization import sanitize


class PreProjetoDetail(ResourceBase):

     def __init__(self):
        super (PreProjetoDetail,self).__init__()

     def get(self, id):

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


        id = id


        try:
            Log.debug('Starting database call')
            results, n_records = PreProjetoModelObject().all(limit, offset, id = id, extra_fields = True)
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

        preprojeto = listify_queryset(results)[0]

        "Sanitizing text values"
        preprojeto['acessibilidade'] = sanitize(preprojeto['acessibilidade'], truncated = False)
        preprojeto['objetivos'] = sanitize(preprojeto['objetivos'], truncated = False)
        preprojeto['justificativa'] = sanitize(preprojeto['justificativa'], truncated = False)
        preprojeto['etapa'] = sanitize(preprojeto['etapa'], truncated = False)
        preprojeto['ficha_tecnica'] = sanitize(preprojeto['ficha_tecnica'], truncated = False)
        preprojeto['impacto_ambiental'] = sanitize(preprojeto['impacto_ambiental'], truncated = False)
        preprojeto['especificacao_tecnica'] = sanitize(preprojeto['especificacao_tecnica'], truncated = False)
        preprojeto['estrategia_execucao'] = sanitize(preprojeto['estrategia_execucao'], truncated = False)
        preprojeto['democratizacao'] =  sanitize(preprojeto["democratizacao"], truncated = False)

        preprojeto['sinopse'] = sanitize(preprojeto["sinopse"], truncated = False)
        preprojeto['resumo'] = sanitize(preprojeto["resumo"], truncated = False)

        return self.render(preprojeto, headers)
