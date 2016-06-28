from ResourceBase import *
from input_validation import validate_input
import json

class TestResource(ResourceBase):

    def __init__(self):
        pass


    def get(self):
        result =  {'content' : 'API is up and running :D'}
        schema = open("resources/test_input_schema.json").read()
        validate_input(request.args, json.loads(schema) )

        #print json.dumps(request.args)
        #print json.loads(schema)

        return result
