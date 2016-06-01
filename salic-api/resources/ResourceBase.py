from result_format import get_formated
from flask import Flask, request, make_response, send_file
from flask import Response
from flask_restful import Resource
from database.QueryHandler import QueryHandler
from APIError import APIError
import sys
sys.path.append('../')
from utils.Log import Log
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import GLOBAL_RATE_LIMITS, RATE_LIMITING_ACTIVE
from config import LIMIT_PAGING, OFFSET_PAGING, AVAILABLE_CONTENT_TYPES 


from flask.ext.limiter import HEADERS


app = Flask(__name__)


limiter = Limiter(
    app,
    key_func=get_remote_address,
    headers_enabled = True,
)



shared_limiter = limiter.shared_limit(GLOBAL_RATE_LIMITS, scope="salic_api")

limiter.header_mapping = {
    HEADERS.LIMIT : "X-My-Limit",
    HEADERS.RESET : "X-My-Reset",
    HEADERS.REMAINING: "X-My-Remaining"
}

class ResourceBase(Resource):
    
    if RATE_LIMITING_ACTIVE:
        Log.info('Rate limiting active : %s'%(GLOBAL_RATE_LIMITS))
        decorators = [shared_limiter]
    else:
        Log.info('Rate limiting is turned off')
    
    def __init__(self):
        self.query_handler = QueryHandler()
    
      
    def render(self, data, headers =  {}, status_code  = 200):
        
        if request.headers['Accept'] == 'application/xml':
            response = Response(get_formated(data, 'xml'), content_type='application/xml; charset=utf-8')

        elif request.headers['Accept'] == 'text/csv':
            response = Response(get_formated(data, 'csv'), content_type='text/csv; charset=utf-8')
     
        
        # JSON or invalid Content-Type
        else :
            response = Response(get_formated(data, 'json'), content_type='application/json; charset=utf-8')
            
        
        response.headers.extend(headers)
        response.status_code = status_code
        real_ip = request.headers.get('X-Real-Ip')
        
        if real_ip == None:
            real_ip = ''
             
        Log.info(request.path+' '+real_ip+' '+str(status_code) + ' '+str(response.headers.get('Content-Length')))
        
        return response
    
    
def format_args(hearder_args):
    formated = ''
    
    for key in hearder_args:
        formated = formated + str(key) + ' = ' + hearder_args[key]+' '
    
    return formated
    
    
@app.before_request 
def request_start():
    content_type = request.headers.get('Accept') or ''
    real_ip = request.headers.get('X-Real-Ip') or ''
         
    Log.info(request.path+' '+format_args(request.args)\
                 +' '+real_ip\
                 +' '+content_type)
        
    #Test content_type
        
    # if content_type and content_type not in  AVAILABLE_CONTENT_TYPES:
    #     results = {'message' : 'Content-Type not supported',
    #                 'message_code' : 8
    #             }
    #     return {'error' : 'content-type'}
    #     return self.render(results, status_code = 405)
        
    def test_resource():
        app = Flask(__name__)
        api = Api(app)
        print type(api)
        api.add_resource(Projeto, '/')
        app.run(debug=True)

    if __name__ == '__main__':
        test_resource()
    
        
