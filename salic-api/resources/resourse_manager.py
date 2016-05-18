from flask import Flask
from flask.ext.cors import CORS, cross_origin
from config import BASE_VERSION
from ResourceBase import app
from flask_restful import Api

#Available Resources:
from projeto.Projeto import Projeto
from projeto.Projeto_list import ProjetoList
from projeto.Resumo import Resumo
from projeto.Providencia import Providencia
from projeto.Area import Area
from projeto.Segmento import Segmento
from preprojeto.PreProjeto import PreProjetoList
from proponente.Proponente import Proponente
from projeto.Acessibilidade import Acessibilidade
from projeto.DemocratizacaoDeAcesso import DemocratizacaoDeAcesso
from projeto.FichaTecnica import FichaTecnica
from projeto.Justificativa import Justificativa
from projeto.Objetivos import Objetivos
from projeto.EtapaDeTrabalho import EtapaDeTrabalho
from projeto.Captacoes import Captacoes
from incentivador.Incentivador import Incentivador
from incentivador.Doacao import Doacao

from TestResource import TestResource

api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
 
 
api.add_resource(TestResource, '/test', '/test/')
api.add_resource(Projeto, '/%s/projetos/<string:PRONAC>/'%(BASE_VERSION))
api.add_resource(Area, '/%s/projetos/areas/'%(BASE_VERSION))
api.add_resource(Segmento, '/%s/projetos/segmentos/'%(BASE_VERSION))
api.add_resource(ProjetoList, '/%s/projetos/'%(BASE_VERSION))
api.add_resource(Resumo, '/%s/projetos/<string:PRONAC>/resumo/'%(BASE_VERSION))
api.add_resource(Providencia, '/%s/projetos/<string:PRONAC>/providencia/'%(BASE_VERSION))

api.add_resource(Acessibilidade, '/%s/projetos/<string:PRONAC>/acessibilidade/'%(BASE_VERSION))
api.add_resource(DemocratizacaoDeAcesso, '/%s/projetos/<string:PRONAC>/democratizacao/'%(BASE_VERSION))
api.add_resource(FichaTecnica, '/%s/projetos/<string:PRONAC>/fichatecnica/'%(BASE_VERSION))
api.add_resource(Justificativa, '/%s/projetos/<string:PRONAC>/justificativa/'%(BASE_VERSION))
api.add_resource(Objetivos, '/%s/projetos/<string:PRONAC>/objetivos/'%(BASE_VERSION))
api.add_resource(EtapaDeTrabalho, '/%s/projetos/<string:PRONAC>/etapa/'%(BASE_VERSION))
api.add_resource(Captacoes, '/%s/projetos/<string:PRONAC>/captacoes/'%(BASE_VERSION))

api.add_resource(PreProjetoList, '/%s/preprojetos/'%(BASE_VERSION))

api.add_resource(Proponente, '/%s/proponentes/'%(BASE_VERSION))

api.add_resource(Incentivador, '/%s/incentivadores/'%(BASE_VERSION))
api.add_resource(Doacao, '/%s/incentivadores/<string:cgccpf>/doacoes/'%(BASE_VERSION))