from serialization import serialize
from flask import Flask, request, make_response, send_file
from flask import Response
from flask_restful import Resource
from APIError import APIError
from rate_limiting import shared_limiter
import sys
sys.path.append('../')
from app import app
from utils.Log import Log
from caching import make_key

# import the flask extension
from flask.ext.cache import Cache


class ResourceBase(Resource):

    # Rate limiting setup --------------------

    if app.config['RATE_LIMITING_ACTIVE']:
        Log.info('Rate limiting active : %s'%(app.config['GLOBAL_RATE_LIMITS']))
        decorators = [shared_limiter]
    else:
        Log.info('Rate limiting is turned off')


    # Caching setup --------------------
    if app.config['CACHING_ACTIVE']:
        Log.info('Caching is active')
    else:
        app.config['CACHE_TYPE'] = 'null'
        Log.info('Caching is disabled')
        app.config['CACHE_NO_NULL_WARNING'] = True

    # register the cache instance and binds it on to your app
    app.cache = Cache(app)
    app.cache.clear()

    def __init__(self):

        self.to_hal = None


    def render(self, data, headers =  {}, status_code  = 200, raw = False):

        if request.headers['Accept'] == 'application/xml':
            if raw:
                data = data
            else:
                data = serialize(data, 'xml')
            response = Response(data, content_type='application/xml; charset=utf-8')

        elif request.headers['Accept'] == 'text/csv':
            if raw:
                data = data
            else:
                data = serialize(data, 'csv')

            response = Response(data, content_type='text/csv; charset=utf-8')


        # JSON or invalid Content-Type
        else :
            if raw:
                data = data
            else:
                if self.to_hal is not None and status_code == 200:
                    data = self.to_hal(data)

                data = serialize(data, 'json')

            response = Response(data, content_type='application/hal+json; charset=utf-8')


        response.headers.extend(headers)
        response.status_code = status_code
        real_ip = request.headers.get('X-Real-Ip')

        if real_ip == None:
            real_ip = ''

        Log.info(request.path+' '+real_ip+' '+str(status_code) + ' '+str(response.headers.get('Content-Length')))

        return response


        # Given a cgc/cpf/cnpj, makes sure it return only elements with exact match
    # Used to correct the use of SQL LIKE statement
    def get_unique(self, cgccpf, elements):

        exact_matches = []

        for e in elements: 

            if e['cgccpf'] == cgccpf:
                exact_matches.append(e)

        return exact_matches


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





