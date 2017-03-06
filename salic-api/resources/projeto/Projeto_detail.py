from flask_restful import Api
from flask import Response
from ..ResourceBase import *
from models import (
                    ProjetoModelObject, CertidoesNegativasModelObject,
                    DivulgacaoModelObject,DescolamentoModelObject,
                    DistribuicaoModelObject, AdequacoesPedidoModelObject,
                    AdequacoesParecerModelObject, CaptacaoModelObject
                    )
from ..serialization import listify_queryset
from ..format_utils import truncate, remove_blanks, cgccpf_mask
from ..sanitization import sanitize
import file_attachment
import brand_attachment
from datetime import datetime
from ..security import encrypt




class ProjetoDetail(ResourceBase):

    def build_links(self, args = {}):

        self.links["self"] += args['PRONAC']

        url_id = encrypt(args['proponente_id'])
        proponente_link = app.config['API_ROOT_URL']+'proponentes/%s'%url_id

        incentivadores_link = app.config['API_ROOT_URL']+ 'incentivadores/?PRONAC='+args['PRONAC']
        fornecedores_link = app.config['API_ROOT_URL']+ 'fornecedores/?PRONAC='+args['PRONAC']

        self.links["proponente"] = proponente_link
        self.links["incentivadores"] = incentivadores_link
        self.links["fornecedores"] = fornecedores_link

        self.captacoes_links = []

        for captacao in args['captacoes']:
                captacao_links = {}
                captacao_links['projeto'] = app.config['API_ROOT_URL'] + 'projetos/%s'%args['PRONAC']
                url_id = encrypt(captacao['cgccpf'])
                captacao_links['incentivador'] = app.config['API_ROOT_URL'] + 'incentivadores/?url_id=%s'%url_id

                self.captacoes_links.append(captacao_links)


    def __init__(self):
        super (ProjetoDetail,self).__init__()

        self.links = {
                    "self" : app.config['API_ROOT_URL']+'projetos/',
        }

        def hal_builder(data, args = {}):

            hal_data = data
            
            hal_data['_links']  = self.links

            hal_data['_embedded'] = {'captacoes' : []}

            for index in range(len(data['captacoes'])):
                data['captacoes'][index]['_links'] = self.captacoes_links[index]
                

            hal_data['_embedded']['captacoes'] = data['captacoes']
            del data['captacoes']


            return hal_data


        self.to_hal = hal_builder

    @app.cache.cached(timeout=app.config['GLOBAL_CACHE_TIMEOUT'])
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
            result, n_records = ProjetoModelObject().all(limit=1, offset=0, PRONAC = PRONAC)
            Log.debug('Database call was successful')
        except Exception as e:
            Log.error('Database error trying to fetch \"Project data\"')
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

        Log.debug('IdPRONAC = %s'%str(projeto['IdPRONAC']))

        try:
            certidoes_negativas = CertidoesNegativasModelObject().all(projeto['PRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"certidoes_negativas data\"')
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        projeto['certidoes_negativas'] = listify_queryset(certidoes_negativas)


        try:
            documentos_anexados = ProjetoModelObject().attached_documents(projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"documentos_anexados data\"')
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        documentos_anexados = listify_queryset(documentos_anexados)

        sanitized_documentos = []

        for documento in documentos_anexados:
            link = file_attachment.build_link(documento)

            if link == '':
                continue

            sanitized_doc = {}

            sanitized_doc['link'] = link

            sanitized_doc['classificacao'] = documento['Descricao']
            sanitized_doc['data'] = documento['Data']
            sanitized_doc['nome'] = documento['NoArquivo']

            sanitized_documentos.append(sanitized_doc)

        projeto['documentos_anexados'] = sanitized_documentos

        try:
            marcas_anexadas = ProjetoModelObject().attached_brands(projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"marcas_anexadas data\"')
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        marcas_anexadas = listify_queryset(marcas_anexadas)

        for marca in marcas_anexadas:
            marca['link'] = brand_attachment.build_link(marca)

        projeto['marcas_anexadas'] = marcas_anexadas

        try:
            divulgacao = DivulgacaoModelObject().all(projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"divulgacao data\"')
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        projeto['divulgacao'] = listify_queryset(divulgacao)

        try:
            deslocamentos = DescolamentoModelObject().all(projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"deslocamentos data\"')
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        deslocamentos = listify_queryset(deslocamentos)

        deslocamentos_satitized = []

        for deslocamento in deslocamentos:
            deslocamento_satitized = {}

            deslocamento_satitized['pais_origem'] = deslocamento['PaisOrigem']
            deslocamento_satitized['pais_destino'] = deslocamento['PaisDestino']
            deslocamento_satitized['uf_origem'] = deslocamento['UFOrigem']
            deslocamento_satitized['uf_destino'] = deslocamento['UFDestino']
            deslocamento_satitized['municipio_origem'] = deslocamento['MunicipioOrigem']
            deslocamento_satitized['municipio_destino'] = deslocamento['MunicipioDestino']
            deslocamento_satitized['quantidade'] = deslocamento['Qtde']

            deslocamentos_satitized.append(deslocamento_satitized)

        projeto['deslocamento'] = deslocamentos_satitized

        try:
            distribuicoes = DistribuicaoModelObject().all(projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"distribuicoes data\"')
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        distribuicoes = listify_queryset(distribuicoes)

        distribuicoes_satitized = []

        for distribuicao in distribuicoes:

            distribuicao_satitized = {}

            distribuicao_satitized['area'] = distribuicao['area']
            distribuicao_satitized['segmento'] = distribuicao['segmento']
            distribuicao_satitized['produto'] = distribuicao['produto']
            distribuicao_satitized['posicao_logo'] = distribuicao['posicao_logo']
            distribuicao_satitized['qtd_outros'] = distribuicao['QtdeOutros']
            distribuicao_satitized['qtd_proponente'] = distribuicao['QtdeProponente']
            distribuicao_satitized['qtd_produzida'] = distribuicao['QtdeProduzida']
            distribuicao_satitized['qtd_patrocinador'] = distribuicao['QtdePatrocinador']
            distribuicao_satitized['qtd_venda_normal'] = distribuicao['QtdeVendaNormal']
            distribuicao_satitized['qtd_venda_promocional'] = distribuicao['QtdeVendaPromocional']
            distribuicao_satitized['preco_unitario_normal'] = distribuicao['PrecoUnitarioNormal']
            distribuicao_satitized['preco_unitario_promocional'] = distribuicao['PrecoUnitarioPromocional']

            distribuicao_satitized['localizacao'] = distribuicao['Localizacao']

            distribuicao_satitized['receita_normal'] = distribuicao_satitized['qtd_venda_normal']*distribuicao_satitized['preco_unitario_normal']
            distribuicao_satitized['receita_pro'] = distribuicao_satitized['qtd_venda_promocional']*distribuicao_satitized['preco_unitario_normal']
            distribuicao_satitized['receita_prevista'] = distribuicao_satitized['qtd_venda_normal']*distribuicao_satitized['preco_unitario_normal']+\
                                                       distribuicao_satitized['qtd_venda_promocional']*distribuicao_satitized['preco_unitario_promocional']

            distribuicoes_satitized.append(distribuicao_satitized)


        projeto['distribuicao'] = distribuicoes_satitized

        try:
            readequacoes_pedido = AdequacoesPedidoModelObject().all(projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"readequacoes_pedido data\"')
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        readequacoes_pedido = listify_queryset(readequacoes_pedido)

        for readequacao in readequacoes_pedido:
            readequacao['dsJustificativa'] = sanitize(readequacao['dsJustificativa'], truncated = False)
            readequacao['dsAvaliacao'] = sanitize(readequacao['dsAvaliacao'], truncated = False)
            readequacao['dsSolicitacao'] = sanitize(readequacao['dsSolicitacao'], truncated = False)

        try:
            readequacoes_parecer = AdequacoesParecerModelObject().all(projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"readequacoes_parecer data\"')
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        readequacoes_parecer = listify_queryset(readequacoes_parecer)

        for readequacao in readequacoes_parecer:
            readequacao['dsJustificativa'] = sanitize(readequacao['dsJustificativa'], truncated = False)
            readequacao['dsAvaliacao'] = sanitize(readequacao['dsAvaliacao'], truncated = False)
            readequacao['dsSolicitacao'] = sanitize(readequacao['dsSolicitacao'], truncated = False)

        readequacoes = {}

        readequacoes['pedido'] = readequacoes_pedido
        readequacoes['parecer'] = readequacoes_parecer

        projeto['readequacoes'] = readequacoes

        try:
            prorrogacao = ProjetoModelObject().postpone_request(projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"prorrogacao data\"')
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        prorrogacao = listify_queryset(prorrogacao)
        projeto['prorrogacao'] = prorrogacao

        try:
            relacao_pagamentos = ProjetoModelObject().payments_listing(idPronac = projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"relacao pagamentos data\"')
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        relacao_pagamentos = listify_queryset(relacao_pagamentos)
        projeto['relacao_pagamentos'] = relacao_pagamentos

        try:
            relatorio_fisco = ProjetoModelObject().taxing_report(projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"relatorio fisco data\"')
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        relatorio_fisco = listify_queryset(relatorio_fisco)
        projeto['relatorio_fisco'] = relatorio_fisco

        try:
            relacao_bens_captal = ProjetoModelObject().goods_capital_listing(projeto['IdPRONAC'])
        except Exception as e:
            Log.error('Database error trying to fetch \"relacao bens captal pagamentos data\"')
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        relacao_bens_captal = listify_queryset(relacao_bens_captal)
        projeto['relacao_bens_captal'] = relacao_bens_captal


        try:
            captacoes = CaptacaoModelObject().all(PRONAC = PRONAC)
        except Exception as e:
            Log.error('Database error trying to fetch \"captacoes data\"')
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        captacoes = listify_queryset(captacoes)
        projeto['captacoes'] = captacoes

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

        "Removing IdPRONAC"
        del projeto['IdPRONAC']

        self.build_links(args = {'PRONAC' : projeto['PRONAC'], 'proponente_id' : projeto['cgccpf'], 'captacoes' : projeto['captacoes']})
        projeto['cgccpf'] = cgccpf_mask(projeto['cgccpf'])

        for captacao in projeto['captacoes']:
            captacao['cgccpf'] = cgccpf_mask(captacao['cgccpf'])

        return self.render(projeto)
