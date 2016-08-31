import sys
sys.path.append('../../')
from ..ResourceBase import *
from models import ItemModelObject
from ..serialization import listify_queryset


class Item(ResourceBase):

     def __init__(self):
        super (Item, self).__init__()


     def get(self, cgccpf):

        try:
            results = ItemModelObject().all(cgccpf)
        except Exception as e:
            Log.error( str(e))
            result = {'message' : 'internal error',
                      'message_code' :  17,
                      'more' : 'something is broken'
                      }
            return self.render(result, status_code = 503)

        results = listify_queryset(results)

        if len(results) == 0:

            result = {'message' : 'No items were found with your criteria',
                                 'message_code' : 11}

            return self.render(result, status_code = 404)

        headers = {'X-Total-Count' : len(results)}

        data = results

        return self.render(data, headers)
