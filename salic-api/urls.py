from flask import Flask, redirect
from flask.ext.cors import CORS, cross_origin
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

from resources.fornecedor.Fornecedor import Fornecedor
from resources.fornecedor.Item import Item



from resources.api_doc.SwaggerDef import SwaggerDef


api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

base_version = app.config['BASE_VERSION']

api.add_resource(TestResource, '/test', '/test/')

api.add_resource(ProjetoDetail, '/%s/projetos/<string:PRONAC>/'%(base_version))
api.add_resource(ProjetoList, '/%s/projetos/'%(base_version))
api.add_resource(Proponente, '/%s/proponentes/'%(base_version))
api.add_resource(Captacao, '/%s/projetos/<string:PRONAC>/captacoes/'%(base_version))

api.add_resource(Area, '/%s/projetos/areas/'%(base_version))
api.add_resource(Segmento, '/%s/projetos/segmentos/'%(base_version))

api.add_resource(PreProjetoList, '/%s/preprojetos/'%(base_version))
api.add_resource(PreProjetoDetail, '/%s/preprojetos/<string:id>/'%(base_version))

api.add_resource(Incentivador, '/%s/incentivadores/'%(base_version))
api.add_resource(Doacao, '/%s/incentivadores/<string:cgccpf>/doacoes/'%(base_version))

api.add_resource(Fornecedor, '/%s/fornecedores/'%(base_version))
api.add_resource(Item, '/%s/fornecedores/<string:cgccpf>/itens/'%(base_version))

api.add_resource(SwaggerDef, '/%s/swagger-def/'%(base_version))

@app.route('/')
def documentation():
    return redirect("/doc", code=302)
