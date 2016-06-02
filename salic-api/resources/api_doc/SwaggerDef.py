from ..ResourceBase import *
from config import SWAGGER_DEF_PATH

class SwaggerDef(ResourceBase):

    def __init__(self):
        super (SwaggerDef,self).__init__()

    def get(self):
        swagger_file = open(SWAGGER_DEF_PATH)
        def_data = open(SWAGGER_DEF_PATH).read()

        return self.render(def_data)
