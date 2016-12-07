import sys
sys.path.append('../../')
from ..ResourceBase import *
from models import ProductModelObject
from ..serialization import listify_queryset
from ..security import decrypt

class Product(ResourceBase):

     def __init__(self):
        super (Product, self).__init__()


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

        return self.render(data, headers)
