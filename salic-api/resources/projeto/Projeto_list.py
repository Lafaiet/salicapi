import sys
sys.path.append('../../')
from ..ResourceBase import *
from models import ProjetoModelObject
from ..serialization import listify_queryset
from ..format_utils import truncate, remove_blanks, remove_html_tags, HTMLEntitiesToUnicode, cgccpf_mask
from ..sanitization import sanitize
from Area import Area
from Segmento import Segmento
from ..security import encrypt, decrypt


class ProjetoList(ResourceBase):

    sort_fields = ['ano_projeto', 'PRONAC', 'data_inicio',
                        'data_termino', 'valor_solicitado', 'outras_fontes',
                        'valor_captado', 'valor_proposta', 'valor_aprovado', 'valor_projeto']

    

    def build_links(self, args = {}):

        query_args = '&'

        for arg in request.args:
            if arg!= 'limit' and arg != 'offset':
                query_args+=arg+'='+request.args[arg]+'&'

        if args['offset']-args['limit'] >= 0:
            self.links["prev"] = self.links["self"] + '?limit=%d&offset=%d'%(args['limit'], args['offset']-args['limit'])+query_args
            

        if args['offset']+args['limit'] <= args['last_offset']:
            self.links["next"] = self.links["self"] + '?limit=%d&offset=%d'%(args['limit'], args['offset']+args['limit'])+query_args
        
        self.links["first"] = self.links["self"] + '?limit=%d&offset=0'%(args['limit'])+query_args
        self.links["last"] = self.links["self"] + '?limit=%d&offset=%d'%(args['limit'], args['last_offset'])+query_args
        self.links["self"] += '?limit=%d&offset=%d'%(args['limit'], args['offset'])+query_args

        self.proponents_links = []

        for proponente_id in args['proponentes_ids']:
            url_id = encrypt(proponente_id)
            link = app.config['API_ROOT_URL']+'proponentes/%s'%url_id
            self.proponents_links.append(link)


    def __init__(self):
        super (ProjetoList,self).__init__()
        self.links = {
                    "self" : app.config['API_ROOT_URL']+'projetos/',
        }

        def hal_builder(data, args = {}):
            
            total = args['total']
            count = len(data)

            hal_data = {'_links' : self.links, 'total' : total, 'count' : count}
            
            for p_index in range(len(data)):
                projeto = data[p_index]

                self_link = app.config['API_ROOT_URL']+'projetos/'+projeto['PRONAC']
                proponente_link = self.proponents_links[p_index]
                incentivadores_link = app.config['API_ROOT_URL']+ 'incentivadores/?PRONAC='+projeto['PRONAC']
                fornecedores_link = app.config['API_ROOT_URL']+ 'fornecedores/?PRONAC='+projeto['PRONAC']

                projeto['_links'] = {}
                projeto['_links']['self'] = self_link
                projeto['_links']['proponente'] = proponente_link
                projeto['_links']['incentivadores'] = incentivadores_link
                projeto['_links']['fornecedores'] = fornecedores_link


            hal_data['_embedded'] = {'projetos' : data}
            return hal_data


        self.to_hal = hal_builder

    @app.cache.cached(timeout=app.config['GLOBAL_CACHE_TIMEOUT'], key_prefix=make_key)
    def get(self):

        headers = {}

        if request.args.get('limit') is not None:
            limit = int(request.args.get('limit'))

            if limit > app.config['LIMIT_PAGING']:
                results = {'message' : 'Max limit paging exceeded',
                        'message_code' : 7
                    }
                return self.render(results, status_code = 405)

        else:
            limit = app.config['LIMIT_PAGING']

        if request.args.get('offset') is not None:
            offset = int(request.args.get('offset'))
        else:
            offset = app.config['OFFSET_PAGING']


        PRONAC = None
        nome = None
        proponente = None
        cgccpf = None
        area = None
        segmento = None
        UF = None
        municipio = None
        data_inicio = None
        data_inicio_min = None
        data_inicio_max = None
        data_termino = None
        data_termino_min = None
        data_termino_max = None
        ano_projeto = None
        sort_field = None
        sort_order = None

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

        if request.args.get('proponente_id') is not None:
            cgccpf = decrypt(request.args.get('proponente_id'))

        if request.args.get('area') is not None:
           area = request.args.get('area')

        if request.args.get('segmento') is not None:
            segmento = request.args.get('segmento')

        if request.args.get('segmento') is not None:
            segmento = request.args.get('segmento')

        if request.args.get('UF') is not None:
            UF = request.args.get('UF')

        if request.args.get('municipio') is not None:
            municipio = request.args.get('municipio')

        if request.args.get('data_inicio') is not None:
            data_inicio = request.args.get('data_inicio')

        if request.args.get('data_inicio_min') is not None:
            data_inicio_min = request.args.get('data_inicio_min')

        if request.args.get('data_inicio_max') is not None:
            data_inicio_max = request.args.get('data_inicio_max')

        if request.args.get('data_termino') is not None:
            data_termino = request.args.get('data_termino')

        if request.args.get('data_termino_min') is not None:
            data_termino_min = request.args.get('data_termino_min')

        if request.args.get('data_termino_max') is not None:
            data_termino_max = request.args.get('data_termino_max')

        if request.args.get('ano_projeto') is not None:
            ano_projeto = request.args.get('ano_projeto')

        if request.args.get('sort') is not None:
            sorting = request.args.get('sort').split(':')

            if len(sorting) == 2:
                sort_field = sorting[0]
                sort_order = sorting[1]
            elif len(sorting) == 1:
                sort_field = sorting[0]
                sort_order = 'asc'

            if sort_field not in self.sort_fields:
                Log.error('sorting field error: '+str(sort_field))
                result = {'message' : 'field error: "%s"'%sort_field,
                      'message_code' :  10,
                      }
                return self.render(result, status_code = 405)

        try:
            Log.debug('Starting database call')
            results, n_records = ProjetoModelObject().all(limit, offset, PRONAC, nome,
                              proponente, cgccpf, area, segmento,
                              UF, municipio, data_inicio, data_inicio_min, data_inicio_max,
                              data_termino, data_termino_min, data_termino_max, ano_projeto, sort_field, sort_order)

            Log.debug('Database call was successful')

        except Exception as e:
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  13,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        if n_records == 0 or len(results) == 0:
            results = {'message' : 'No project was found with your criteria',
                        'message_code' : 11
                        }
            return self.render(results, status_code = 404)

        else :
            headers = {'X-Total-Count' : n_records}

        data = listify_queryset(results)

        for projeto in data:

            "Removing IdPRONAC"
            del projeto['IdPRONAC']

            "Getting rid of blanks"
            projeto["cgccpf"]  = remove_blanks(str(projeto["cgccpf"]))

            "Sanitizing text values"
            projeto['acessibilidade'] = sanitize(projeto['acessibilidade'])
            projeto['objetivos'] = sanitize(projeto['objetivos'])
            projeto['etapa'] = sanitize(projeto['etapa'])
            projeto['ficha_tecnica'] = sanitize(projeto['ficha_tecnica'])
            projeto['impacto_ambiental'] = sanitize(projeto['impacto_ambiental'])
            projeto['especificacao_tecnica'] = sanitize(projeto['especificacao_tecnica'])
            projeto['estrategia_execucao'] = sanitize(projeto['estrategia_execucao'])
            projeto['providencia'] = sanitize(projeto['providencia'])
            projeto['democratizacao'] =  sanitize(projeto["democratizacao"])

            projeto['sinopse'] = sanitize(projeto["sinopse"],  truncated = False)
            projeto['resumo'] = sanitize(projeto["resumo"],  truncated = False)
            projeto['justificativa'] = sanitize(projeto['justificativa'])

        if cgccpf is not None:
            data = self.get_unique(cgccpf, data)

        proponentes_ids = []

        for projeto_index in range(len(data)):
            proponentes_ids.append(projeto['cgccpf'])
            data[projeto_index]['cgccpf'] = cgccpf_mask(data[projeto_index]['cgccpf'])

        self.build_links(args = {'limit' : limit, 'offset' : offset, 'proponentes_ids' : proponentes_ids, 'last_offset' : n_records-1})

        return self.render(data, headers)
