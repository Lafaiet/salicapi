from flask import Flask, redirect
from flask.ext.cors import CORS, cross_origin
from app import app
from flask_restful import Api

#Available Resources:

from resources.TestResource import TestResource

from resources.projeto.Projeto_detail import ProjetoDetail
from resources.projeto.Projeto_list import ProjetoList
from resources.projeto.Captacao import Captacao

from resources.projeto.Area import Area
from resources.projeto.Segmento import Segmento

from resources.proponente.Proponente_list import ProponenteList
from resources.proponente.Proponente_detail import ProponenteDetail



from resources.preprojeto.PreProjeto_list import PreProjetoList
from resources.preprojeto.PreProjeto_detail import PreProjetoDetail

from resources.incentivador.Incentivador_list import IncentivadorList
from resources.incentivador.Incentivador_detail import IncentivadorDetail
from resources.incentivador.Doacao import Doacao

from resources.fornecedor.Fornecedor_list import FornecedorList
from resources.fornecedor.Fornecedor_detail import FornecedorDetail

from resources.fornecedor.Produto import Produto



from resources.api_doc.SwaggerDef import SwaggerDef


api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

base_version = app.config['BASE_VERSION']

api.add_resource(TestResource, '/test', '/test/')

api.add_resource(ProjetoDetail, '/%s/projetos/<string:PRONAC>/'%(base_version))
api.add_resource(ProjetoList, '/%s/projetos/'%(base_version))

api.add_resource(ProponenteList, '/%s/proponentes/'%(base_version))
api.add_resource(ProponenteDetail, '/%s/proponentes/<string:proponente_id>/'%(base_version))


api.add_resource(Captacao, '/%s/projetos/<string:PRONAC>/captacoes/'%(base_version))

api.add_resource(Area, '/%s/projetos/areas/'%(base_version))
api.add_resource(Segmento, '/%s/projetos/segmentos/'%(base_version))

api.add_resource(PreProjetoList, '/%s/propostas/'%(base_version))
api.add_resource(PreProjetoDetail, '/%s/propostas/<string:id>/'%(base_version))

api.add_resource(IncentivadorList, '/%s/incentivadores/'%(base_version))
api.add_resource(IncentivadorDetail, '/%s/incentivadores/<string:incentivador_id>/'%(base_version))
api.add_resource(Doacao, '/%s/incentivadores/<string:incentivador_id>/doacoes/'%(base_version))

api.add_resource(FornecedorList, '/%s/fornecedores/'%(base_version))
api.add_resource(FornecedorDetail, '/%s/fornecedores/<string:fornecedor_id>/'%(base_version))
api.add_resource(Produto, '/%s/fornecedores/<string:fornecedor_id>/produtos/'%(base_version))

api.add_resource(SwaggerDef, '/%s/swagger-def/'%(base_version))

@app.route('/')
def documentation():
    return redirect("/doc", code=302)
