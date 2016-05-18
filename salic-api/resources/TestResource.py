from ResourceBase import *

class TestResource(ResourceBase):
    
    def __init__(self):
        pass
    

    def get(self):
        result =  {'content' : 'API is up and running :D'}
        return result