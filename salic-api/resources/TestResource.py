from ResourceBase import *
from input_validation import validate_input
import json
from datetime import datetime

class TestResource(ResourceBase):

    def __init__(self):
        pass

    @app.cache.cached(timeout=300)  # cache this view for 5 minutes
    def get(self):
        timestamp = str(datetime.now())
        result =  {'content' : 'API is up and running :D', 'timestamp' : timestamp}
        #schema = open("resources/test_input_schema.json").read()
        #validate_input(request.args, json.loads(schema) )

        #print json.dumps(request.args)
        #print json.loads(schema)

        return result
