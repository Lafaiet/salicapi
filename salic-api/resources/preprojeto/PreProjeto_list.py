
import sys
sys.path.append('../../')
from ..ResourceBase import *
from models import PreProjetoModelObject
from ..serialization import listify_queryset
from ..sanitization import sanitize


class PreProjetoList(ResourceBase):

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


     def __init__(self):
        super (PreProjetoList,self).__init__()

        self.links = {
                    "self" : app.config['API_ROOT_URL']+'propostas/',
        }

        def hal_builder(data, args = {}):
            
            total = args['total']
            count = len(data)

            hal_data = {'_links' : self.links, 'total' : total, 'count' : count}

            for p_index in range(len(data)):
                proposta = data[p_index]

                self_link = app.config['API_ROOT_URL']+'propostas/'+str(proposta['id'])

                proposta['_links'] = {}
                proposta['_links']['self'] = self_link
                
            hal_data['_embedded'] = {'propostas' : data}

            return hal_data


        self.to_hal = hal_builder

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

        if n_records == 0 or len(results) == 0:
            results = {'message' : 'No pre project was found with your criteria',
                        'message_code' : 11
                        }
            return self.render(results, status_code = 404)

        else :
            headers = {'X-Total-Count' : n_records}

        data = listify_queryset(results)

        for preprojeto in data:

            #Sanitizing text values
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

        self.build_links(args = {'limit' : limit, 'offset' : offset, 'last_offset' : n_records-1})

        return self.render(data, headers)
