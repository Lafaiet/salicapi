from flask import Flask
from flask.ext.cors import CORS, cross_origin
from config import BASE_VERSION
from app import app
from flask_restful import Api

#Available Resources:

from resources.TestResource import TestResource

from resources.projeto.Projeto_detail import ProjetoDetail
from resources.projeto.Projeto_list import ProjetoList
from resources.proponente.Proponente import Proponente
from resources.projeto.Captacao import Captacao

from resources.projeto.Area import Area
from resources.projeto.Segmento import Segmento

from resources.preprojeto.PreProjeto_list import PreProjetoList
from resources.preprojeto.PreProjeto_detail import PreProjetoDetail

from resources.incentivador.Incentivador import Incentivador
from resources.incentivador.Doacao import Doacao

from resources.api_doc.SwaggerDef import SwaggerDef


api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


api.add_resource(TestResource, '/test', '/test/')

api.add_resource(ProjetoDetail, '/%s/projetos/<string:PRONAC>/'%(BASE_VERSION))
api.add_resource(ProjetoList, '/%s/projetos/'%(BASE_VERSION))
api.add_resource(Proponente, '/%s/proponentes/'%(BASE_VERSION))
api.add_resource(Captacao, '/%s/projetos/<string:PRONAC>/captacoes/'%(BASE_VERSION))

api.add_resource(Area, '/%s/projetos/areas/'%(BASE_VERSION))
api.add_resource(Segmento, '/%s/projetos/segmentos/'%(BASE_VERSION))

api.add_resource(PreProjetoList, '/%s/preprojetos/'%(BASE_VERSION))
api.add_resource(PreProjetoDetail, '/%s/preprojetos/<string:id>/'%(BASE_VERSION))

api.add_resource(Incentivador, '/%s/incentivadores/'%(BASE_VERSION))
api.add_resource(Doacao, '/%s/incentivadores/<string:cgccpf>/doacoes/'%(BASE_VERSION))

api.add_resource(SwaggerDef, '/%s/swagger-def/'%(BASE_VERSION))
