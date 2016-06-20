from serialization import serialize
from flask import Flask, request, make_response, send_file
from flask import Response
from flask_restful import Resource
from APIError import APIError
from rate_limiting import shared_limiter, GLOBAL_RATE_LIMITS, RATE_LIMITING_ACTIVE
import sys
sys.path.append('../')
from app import app
from utils.Log import Log
from config import LIMIT_PAGING, OFFSET_PAGING, AVAILABLE_CONTENT_TYPES


class ResourceBase(Resource):

    if RATE_LIMITING_ACTIVE:
        Log.info('Rate limiting active : %s'%(GLOBAL_RATE_LIMITS))
        decorators = [shared_limiter]
    else:
        Log.info('Rate limiting is turned off')

    def __init__(self):
        pass


    def render(self, data, headers =  {}, status_code  = 200):

        if request.headers['Accept'] == 'application/xml':
            response = Response(serialize(data, 'xml'), content_type='application/xml; charset=utf-8')

        elif request.headers['Accept'] == 'text/csv':
            response = Response(serialize(data, 'csv'), content_type='text/csv; charset=utf-8')


        # JSON or invalid Content-Type
        else :
            response = Response(serialize(data, 'json'), content_type='application/json; charset=utf-8')


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
