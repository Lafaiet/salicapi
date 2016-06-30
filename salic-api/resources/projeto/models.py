# -*- coding: utf-8 -*-

from sqlalchemy import case, func

from ..ModelsBase import ModelsBase
from ..SharedModels import AreaModel, SegmentoModel
from ..SharedModels import (ProjetoModel, InteressadoModel, MecanismoModel,
                            SituacaoModel, PreProjetoModel, EnquadramentoModel,
                            PreProjetoModel, CaptacaoModel, CertidoesNegativasModel
                            )


import sys
sys.path.append('../../')
from utils.Timer import Timer
from utils.Log import Log



class ProjetoModelObject(ModelsBase):

    def __init__(self):
        super (ProjetoModelObject, self).__init__()

    def all(self, limit, offset, PRONAC = None, nome = None, proponente = None,
                          cgccpf = None, area = None, segmento = None,
                          UF = None, municipio = None, data_inicio = None,
                          data_inicio_min = None, data_inicio_max = None,
                          data_termino = None, data_termino_min = None,
                          data_termino_max = None, extra_fields = False, ano_projeto = None):

        start_row = offset
        end_row = offset+limit

        if extra_fields:
            additional_fields =  (
                             PreProjetoModel.Acessibilidade.label('acessibilidade'),
                             PreProjetoModel.Objetivos.label('objetivos'),
                             PreProjetoModel.Justificativa.label('justificativa'),
                             PreProjetoModel.DemocratizacaoDeAcesso.label('democratizacao'),
                             PreProjetoModel.EtapaDeTrabalho.label('etapa'),
                             PreProjetoModel.FichaTecnica.label('ficha_tecnica'),
                             PreProjetoModel.ResumoDoProjeto.label('resumo'),
                             PreProjetoModel.Sinopse.label('sinopse'),
                             PreProjetoModel.ImpactoAmbiental.label('impacto_ambiental'),
                             PreProjetoModel.EspecificacaoTecnica.label('especificacao_tecnica'),
                             PreProjetoModel.EstrategiadeExecucao.label('estrategia_execucao'),

                             ProjetoModel.ProvidenciaTomada.label('providencia'),
                             )
        else:
            additional_fields = ()


        valor_proposta_case = case([(ProjetoModel.IdPRONAC != None, func.sac.dbo.fnValorDaProposta(ProjetoModel.IdPRONAC)),],
        else_ = func.sac.dbo.fnValorSolicitado(ProjetoModel.AnoProjeto, ProjetoModel.Sequencial))

        valor_aprovado_case = case([(ProjetoModel.Mecanismo == '2' or ProjetoModel.Mecanismo == '6', func.sac.dbo.fnValorAprovadoConvenio(ProjetoModel.AnoProjeto,ProjetoModel.Sequencial)),],
        else_ = func.sac.dbo.fnValorAprovado(ProjetoModel.AnoProjeto,ProjetoModel.Sequencial))

        valor_projeto_case = case([(ProjetoModel.Mecanismo =='2' or ProjetoModel.Mecanismo =='6', func.sac.dbo.fnValorAprovadoConvenio(ProjetoModel.AnoProjeto,ProjetoModel.Sequencial)),],
        else_ = func.sac.dbo.fnValorAprovado(ProjetoModel.AnoProjeto,ProjetoModel.Sequencial) + func.sac.dbo.fnOutrasFontes(ProjetoModel.IdPRONAC))

        enquadramento_case = case([(EnquadramentoModel.Enquadramento == '1', 'Artigo 26'),
                                   (EnquadramentoModel.Enquadramento == '2', 'Artigo 18')
                                   ],
        else_ = 'Nao enquadrado')

        ano_case = case([(ProjetoModel.Mecanismo =='2' or ProjetoModel.Mecanismo =='6', func.sac.dbo.fnValorAprovadoConvenio(ProjetoModel.AnoProjeto,ProjetoModel.Sequencial)),],
        else_ = func.sac.dbo.fnValorAprovado(ProjetoModel.AnoProjeto,ProjetoModel.Sequencial))

        with Timer(action = 'Database query for get_projeto_list method', verbose = True):
          res= self.sql_connector.session.query(
                                                  ProjetoModel.NomeProjeto.label('nome'),
                                                  ProjetoModel.PRONAC,
                                                  ProjetoModel.AnoProjeto.label('ano_projeto'),
                                                  ProjetoModel.UfProjeto.label('UF'),
                                                  InteressadoModel.Cidade.label('municipio'),
                                                  ProjetoModel.DtInicioExecucao.label('data_inicio'),
                                                  ProjetoModel.DtFimExecucao.label('data_termino'),

                                                  AreaModel.Descricao.label('area'),
                                                  SegmentoModel.Descricao.label('segmento'),
                                                  SituacaoModel.Descricao.label('situacao'),
                                                  InteressadoModel.Nome.label('proponente'),
                                                  InteressadoModel.CgcCpf.label('cgccpf'),
                                                  MecanismoModel.Descricao.label('mecanismo'),

                                                  func.sac.dbo.fnValorSolicitado(ProjetoModel.AnoProjeto, ProjetoModel.Sequencial).label('valor_solicitado'),
                                                  func.sac.dbo.fnOutrasFontes(ProjetoModel.IdPRONAC).label('outras_fontes'),
                                                  func.sac.dbo.fnCustoProjeto (ProjetoModel.AnoProjeto, ProjetoModel.Sequencial).label('valor_captado'),
                                                  valor_proposta_case.label('valor_proposta'),
                                                  valor_aprovado_case.label('valor_aprovado'),
                                                  valor_projeto_case.label('valor_projeto'),

                                                  enquadramento_case.label('enquadramento'),

                                                  *additional_fields

                                                  ).join(AreaModel)\
                                                  .join(SegmentoModel)\
                                                  .join(SituacaoModel)\
                                                  .join(InteressadoModel)\
                                                  .join(PreProjetoModel)\
                                                  .join(MecanismoModel)\
                                                  .outerjoin(EnquadramentoModel, EnquadramentoModel.IdPRONAC ==  ProjetoModel.IdPRONAC)\
                                                  .order_by(ProjetoModel.IdPRONAC)

        if PRONAC is not None:
            res = res.filter(ProjetoModel.PRONAC == PRONAC)

        if area is not None:
            res = res.filter(AreaModel.Descricao == area)

        if segmento is not None:
            res = res.filter(SegmentoModel.Descricao == segmento)

        if proponente is not None:
            res = res.filter(InteressadoModel.Nome.like('%' + proponente + '%'))

        if cgccpf is not None:
            res = res.filter(InteressadoModel.CgcCpf.like('%' + cgccpf + '%') )

        if nome is not None:
            res = res.filter(ProjetoModel.NomeProjeto.like('%' + nome + '%'))

        if UF is not None:
            res = res.filter(InteressadoModel.Uf == UF)

        if municipio is not None:
            res = res.filter(InteressadoModel.Cidade == municipio)

        if data_inicio is not None:
            res = res.filter(ProjetoModel.DtInicioExecucao == data_inicio)

        if data_inicio_min is not None:
            res = res.filter(ProjetoModel.DtInicioExecucao >= data_inicio_min)

        if data_inicio_max is not None:
            res = res.filter(ProjetoModel.DtInicioExecucao <= data_inicio_max)

        if data_termino is not None:
            res = res.filter(ProjetoModel.DtFimExecucao == data_termino)

        if data_termino_min is not None:
            res = res.filter(ProjetoModel.DtFimExecucao >= data_termino_min)

        if data_termino_max is not None:
            res = res.filter(ProjetoModel.DtFimExecucao <= data_termino_max)

        if ano_projeto is not None:
            res = res.filter(ProjetoModel.AnoProjeto == ano_projeto)

        with Timer(action = 'Projects count() fast ', verbose = True):
          total_records = self.count(res)

        # with Timer(action = 'Projects count() slow ', verbose = True):
        #   total_records = res.count()
        #   #Log.debug("total : "+str(total_records))

        with Timer(action = 'Projects slice()', verbose = True):
          res = res.slice(start_row, end_row)

        return res.all(), total_records



class CaptacaoModelObject(ModelsBase):

    def all(self, PRONAC):

        res = self.sql_connector.session.query(
                                               CaptacaoModel.CaptacaoReal.label('valor'),
                                               CaptacaoModel.DtRecibo.label('data_recibo'),
                                               InteressadoModel.Nome.label('nome_doador'),
                                               CaptacaoModel.CgcCpfMecena.label('cgccpf'),
                                              ).join(ProjetoModel, CaptacaoModel.PRONAC==ProjetoModel.PRONAC)\
                                                .join(InteressadoModel, CaptacaoModel.CgcCpfMecena==InteressadoModel.CgcCpf)\




        if PRONAC is not None:
            res = res.filter(CaptacaoModel.PRONAC == PRONAC)

        return res.all()



class AreaModelObject(ModelsBase):

    def __init__(self):
        super (AreaModelObject,self).__init__()

    def all(self):
        res  = self.sql_connector.session.query(AreaModel.Descricao.label('area'))
        return res.all()



class SegmentoModelObject(ModelsBase):

    def __init__(self):
        super (SegmentoModelObject,self).__init__()


    def all(self):
        res  = self.sql_connector.session.query(SegmentoModel.Descricao.label('segmento'))
        return res.all()

class CertidoesNegativasModelObject(ModelsBase):

    def __init__(self):
        super (CertidoesNegativasModelObject,self).__init__()


    def all(self, PRONAC = None, CgcCpf = None):

        descricao_case = case([
                                (CertidoesNegativasModel.CodigoCertidao == '49', u'Quitação de Tributos Federais'),
                                (CertidoesNegativasModel.CodigoCertidao == '51', 'FGTS'),
                                (CertidoesNegativasModel.CodigoCertidao == '52', 'INSS'),
                                (CertidoesNegativasModel.CodigoCertidao == '244', 'CADIN'),
        ])

        situacao_case = case([(CertidoesNegativasModel.cdSituacaoCertidao == 0, u'Pendente')],
        else_ = u'Não Pendente'
        )

        res  = self.sql_connector.session.query(CertidoesNegativasModel.DtEmissao.label('data_emissao'),
                                                CertidoesNegativasModel.DtValidade.label('data_validade'),
                                                descricao_case.label('descricao'),
                                                situacao_case.label('situacao'),
                                                )

        if PRONAC is not None:
            res = res.filter(CertidoesNegativasModel.PRONAC == PRONAC)

        return res.all()
