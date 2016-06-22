from flask_restful import Api
from flask import Response
from ..ResourceBase import *
from models import ProjetoModelObject
from ..serialization import listify_queryset
from ..format_utils import truncate, remove_blanks
from sanitization import sanitize




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
            result, n_records = ProjetoModelObject().all(limit=1, offset=0, PRONAC = PRONAC, extra_fields = True)
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

        projeto = listify_queryset(result)[0]

        "Getting rid of blanks"
        projeto["cgccpf"]  = remove_blanks(str(projeto["cgccpf"]))

        "Sanitizing text values"
        projeto['acessibilidade'] = sanitize(projeto['acessibilidade'])
        projeto['objetivos'] = sanitize(projeto['objetivos'])
        projeto['justificativa'] = sanitize(projeto['justificativa'])
        projeto['etapa'] = sanitize(projeto['etapa'])
        projeto['ficha_tecnica'] = sanitize(projeto['ficha_tecnica'])
        projeto['impacto_ambiental'] = sanitize(projeto['impacto_ambiental'])
        projeto['especificacao_tecnica'] = sanitize(projeto['especificacao_tecnica'])
        projeto['estrategia_execucao'] = sanitize(projeto['estrategia_execucao'])
        projeto['providencia'] = sanitize(projeto['providencia'])
        projeto['democratizacao'] =  sanitize(projeto["democratizacao"])

        projeto['sinopse'] = truncate(projeto["sinopse"])
        projeto['resumo'] = truncate(projeto["resumo"])

        return self.render(projeto)
