import sys
sys.path.append('../../')
from ..ResourceBase import *
from models import ProductModelObject
from ..serialization import listify_queryset
from ..security import decrypt, encrypt
from ..format_utils import remove_blanks, cgccpf_mask


class Product(ResourceBase):

     def build_links(self, args = {}):

        self.links = {'self' : ''}

        self.links["self"] = app.config['API_ROOT_URL'] + 'fornecedores/%s/produtos/'%args['url_id']

        self.produtos_links = []

        for produto in args['produtos']:
                produto_links = {}
                produto_links['projeto'] = app.config['API_ROOT_URL'] + 'projetos/%s'%produto['PRONAC']
                url_id = encrypt(produto['cgccpf'])
                produto_links['fornecedor'] = app.config['API_ROOT_URL'] + 'fornecedores/?url_id=%s'%url_id

                self.produtos_links.append(produto_links)

     def __init__(self):
        super (Product, self).__init__()

        def hal_builder(data, args = {}):

            hal_data = {'_links' : ''}
            
            hal_data['_links']  = self.links

            hal_data['_embedded'] = {'produtos' : ''}

            for index in range(len(data)):
                produto = data[index]
                produto['_links'] = self.produtos_links[index]
                
            hal_data['_embedded']['produtos'] = data

            return hal_data

        self.to_hal = hal_builder


     def get(self, url_id):
      
        cgccpf = decrypt(url_id)

        try:
            results = ProductModelObject().all(cgccpf)
        except Exception as e:
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  17,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        results = listify_queryset(results)

        if len(results) == 0:

            result = {'message' : 'No Products were found with your criteria',
                                 'message_code' : 11}

            return self.render(result, status_code = 404)

        headers = {'X-Total-Count' : len(results)}

        data = results

        for produto in data:
            produto["cgccpf"] = remove_blanks(produto['cgccpf'])

        data = self.get_unique(cgccpf, data)


        self.build_links(args = {'url_id' : url_id, 'produtos' : data})

        for produto in data:
            produto["cgccpf"] = cgccpf_mask(produto["cgccpf"])

        return self.render(data, headers)
