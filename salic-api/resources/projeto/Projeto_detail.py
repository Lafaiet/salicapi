from flask_restful import Api
from flask import Response
from ..ResourceBase import *
from models import ProjetoModelObject, CertidoesNegativasModelObject
from ..serialization import listify_queryset
from ..format_utils import truncate, remove_blanks
from ..sanitization import sanitize
from file_attachment import build_link




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

        try:
            certidoes_negativas = CertidoesNegativasModelObject().all(projeto['PRONAC'])
        except Exception as e:
            Log.error( str(e))

        projeto['certidoes_negativas'] = listify_queryset(certidoes_negativas)

        # if len(certidoes_negativas) == 0:
        #     certidoes_negativas = None
        # else:
        #     certidoes_negativas = listify_queryset(certidoes_negativas)

        try:
            documentos_anexados = ProjetoModelObject().attached_documents(projeto['IdPRONAC'])
        except Exception as e:
            Log.error( str(e))

        documentos_anexados = listify_queryset(documentos_anexados)

        sanitized_documentos = []

        for documento in documentos_anexados:
            link = build_link(documento)

            if link == '':
                continue

            sanitized_doc = {}

            sanitized_doc['link'] = link

            sanitized_doc['classificacao'] = documento['Descricao']
            sanitized_doc['data'] = documento['Data']
            sanitized_doc['nome'] = documento['NoArquivo']

            sanitized_documentos.append(sanitized_doc)

        projeto['documentos_anexados'] = sanitized_documentos

        "Removing IdPRONAC"
        del projeto['IdPRONAC']

        "Getting rid of blanks"
        projeto["cgccpf"]  = remove_blanks(str(projeto["cgccpf"]))

        "Sanitizing text values"
        projeto['acessibilidade'] = sanitize(projeto['acessibilidade'], truncated = False)
        projeto['objetivos'] = sanitize(projeto['objetivos'], truncated = False)
        projeto['justificativa'] = sanitize(projeto['justificativa'], truncated = False)
        projeto['etapa'] = sanitize(projeto['etapa'], truncated = False)
        projeto['ficha_tecnica'] = sanitize(projeto['ficha_tecnica'], truncated = False)
        projeto['impacto_ambiental'] = sanitize(projeto['impacto_ambiental'], truncated = False)
        projeto['especificacao_tecnica'] = sanitize(projeto['especificacao_tecnica'], truncated = False)
        projeto['estrategia_execucao'] = sanitize(projeto['estrategia_execucao'], truncated = False)
        projeto['providencia'] = sanitize(projeto['providencia'], truncated = False)
        projeto['democratizacao'] =  sanitize(projeto["democratizacao"], truncated = False)

        projeto['sinopse'] = sanitize(projeto["sinopse"], truncated = False)
        projeto['resumo'] = sanitize(projeto["resumo"], truncated = False)

        return self.render(projeto)
