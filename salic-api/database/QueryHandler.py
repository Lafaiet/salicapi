from connectors.mssql_connector import MSSql_connector
from sqlalchemy import case, func
from models import *
from sqlalchemy.orm.util import outerjoin
import sys
sys.path.append('../')
from utils.Timer import Timer
from utils.Log import Log

import time

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class QueryHandler():

    def __init__(self):
        self.sql_connector = MSSql_connector()


    def query_wrapper(self, params = None ):
      return self.sql_connector.session.query(params)

    def get_count(self, q):
      count_q = q.statement.with_only_columns([func.count()]).order_by(None)
      count = q.session.execute(count_q).scalar()
      return count

    def get_by_PRONAC(self, PRONAC, extra_fields):
        res, dummy = self.get_projeto_list(limit=1, offset=0, PRONAC = PRONAC, extra_fields = extra_fields)

        return res[0] if res else None

    def get_area(self):
        try:
          with Timer(action = 'Database query for get_area method', verbose = True):
            res  = self.sql_connector.session.query(AreaModel.Descricao.label('area'))
          return res.all()
        except Exception as e:
          Log.error("Database connection error : " + str(e))
          raise e

    def get_segmento(self):
        res  = self.sql_connector.session.query(SegmentoModel.Descricao.label('segmento'))
        return res.all()

    def get_resumo(self, PRONAC):
        res  = self.sql_connector.session.query(ProjetoModel.ResumoProjeto.label('resumo')).filter(ProjetoModel.PRONAC == PRONAC)
        return res.one_or_none()

    def get_acessibilidade(self, PRONAC):
        res  = self.sql_connector.session.query(PreProjetoModel.Acessibilidade.label('acessibilidade')).join(ProjetoModel).filter(ProjetoModel.PRONAC == PRONAC)
        return res.one_or_none()

    def get_objetivos(self, PRONAC):
        res  = self.sql_connector.session.query(PreProjetoModel.Objetivos.label('objetivos')).join(ProjetoModel).filter(ProjetoModel.PRONAC == PRONAC)
        return res.one_or_none()

    def get_justificativa(self, PRONAC):
        res  = self.sql_connector.session.query(PreProjetoModel.Justificativa.label('justificativa')).join(ProjetoModel).filter(ProjetoModel.PRONAC == PRONAC)
        return res.one_or_none()

    def get_democratizacao_de_acesso(self, PRONAC):
        res  = self.sql_connector.session.query(PreProjetoModel.DemocratizacaoDeAcesso.label('democratizacao_de_acesso')).join(ProjetoModel).filter(ProjetoModel.PRONAC == PRONAC)
        return res.one_or_none()

    def get_etapa_de_trabalho(self, PRONAC):
        res  = self.sql_connector.session.query(PreProjetoModel.EtapaDeTrabalho.label('etapa_de_trabalho')).join(ProjetoModel).filter(ProjetoModel.PRONAC == PRONAC)
        return res.one_or_none()

    def get_ficha_tecnica(self, PRONAC):
        res  = self.sql_connector.session.query(PreProjetoModel.FichaTecnica.label('FichaTecnica')).join(ProjetoModel).filter(ProjetoModel.PRONAC == PRONAC)
        return res.one_or_none()

    def get_providencia(self, PRONAC):
        res  = self.sql_connector.session.query(ProjetoModel.ProvidenciaTomada.label('providencia')).filter(ProjetoModel.PRONAC == PRONAC)
        return res.one_or_none()

    def get_proponente(self,  limit, offset, nome = None, cgccpf = None, municipio = None,
                       UF = None, tipo_pessoa = None, all_fields = False):

        start_row = offset
        end_row = offset+limit


        tipo_pessoa_case = case([(InteressadoModel.tipoPessoa=='1', 'fisica'),],
        else_ = 'juridica')

        res= self.sql_connector.session.query(
                                               InteressadoModel.Nome.label('nome'),
                                               InteressadoModel.Cidade.label('municipio'),
                                               InteressadoModel.Uf.label('UF'),
                                               InteressadoModel.Responsavel.label('responsavel'),
                                               InteressadoModel.CgcCpf.label('cgccpf'),
                                               tipo_pessoa_case.label('tipo_pessoa'),
                                               func.count(ProjetoModel.PRONAC).label('quantidade_projetos'),
                                               ).join(ProjetoModel)\
                                                .group_by(InteressadoModel.Nome,
                                                          InteressadoModel.Cidade,
                                                          InteressadoModel.Uf,
                                                          InteressadoModel.Responsavel,
                                                          InteressadoModel.CgcCpf,
                                                          tipo_pessoa_case,
                                                  )\
                                                .order_by(InteressadoModel.CgcCpf)


        if cgccpf is not None:
            res = res.filter(InteressadoModel.CgcCpf.like('%' + cgccpf + '%'))

        if nome is not None:
            res = res.filter(InteressadoModel.Nome.like('%' + nome + '%'))

        if UF is not None:
            res = res.filter(InteressadoModel.Uf == UF)

        if municipio is not None:
            res = res.filter(InteressadoModel.Cidade == municipio)

        if tipo_pessoa is not None:
            if tipo_pessoa == 'fisica':
                tipo_pessoa = '1'
            else:
                tipo_pessoa = '2'

            res = res.filter(InteressadoModel.tipoPessoa == tipo_pessoa )

        total_records = res.count()

        res = res.slice(start_row, end_row)

        return res.all(), total_records


    def get_incentivador(self,  limit, offset, nome = None, cgccpf = None, municipio = None, UF = None, tipo_pessoa = None):

        start_row = offset
        end_row = offset+limit

        tipo_pessoa_case = case([(InteressadoModel.tipoPessoa=='1', 'fisica'),],
        else_ = 'juridica')

        res= self.sql_connector.session.query(
                                               InteressadoModel.Nome.label('nome'),
                                               InteressadoModel.Cidade.label('municipio'),
                                               InteressadoModel.Uf.label('UF'),
                                               InteressadoModel.Responsavel.label('responsavel'),
                                               InteressadoModel.CgcCpf.label('cgccpf'),
                                               func.sum(CaptacaoModel.CaptacaoReal).label('total_doado'),
                                               tipo_pessoa_case.label('tipo_pessoa'),
                                               ).join(CaptacaoModel)\
                                               .group_by(InteressadoModel.Nome,
                                                         InteressadoModel.Cidade,
                                                         InteressadoModel.Uf,
                                                         InteressadoModel.Responsavel,
                                                         InteressadoModel.CgcCpf,
                                                         tipo_pessoa_case
                                                          )\
                                               .order_by(InteressadoModel.CgcCpf)

        if cgccpf is not None:
            res = res.filter(InteressadoModel.CgcCpf.like('%' + cgccpf + '%') )

        if nome is not None:
            res = res.filter(InteressadoModel.Nome.like('%' + nome + '%'))

        if UF is not None:
            res = res.filter(InteressadoModel.Uf == UF)

        if municipio is not None:
            res = res.filter(InteressadoModel.Cidade == municipio)

        if tipo_pessoa is not None:
            if tipo_pessoa == 'fisica':
                tipo_pessoa = '1'
            else:
                tipo_pessoa = '2'

            res = res.filter(InteressadoModel.tipoPessoa == tipo_pessoa )

        total_records = res.count()

        res = res.slice(start_row, end_row)

        return res.all(), total_records


    def get_projeto_list(self, limit, offset, PRONAC = None, nome = None, proponente = None,
                          cgccpf = None, area = None, segmento = None,
                          UF = None, municipio = None, data_inicio = None, data_termino = None, extra_fields = False,
                          ano_projeto = None):

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

        if data_termino is not None:
            res = res.filter(ProjetoModel.DtFimExecucao == data_termino)

        if ano_projeto is not None:
            res = res.filter(ProjetoModel.AnoProjeto == ano_projeto)

        with Timer(action = 'Projects count() fast ', verbose = True):
          total_records = self.get_count(res)

        # with Timer(action = 'Projects count() slow ', verbose = True):
        #   total_records = res.count()
        #   #Log.debug("total : "+str(total_records))

        with Timer(action = 'Projects slice()', verbose = True):
          res = res.slice(start_row, end_row)

        return res.all(), total_records


    def get_preprojeto_list(self, limit, offset, id = None, nome = None, data_inicio = None, data_termino = None, extra_fields = False):

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
                               )
          else:
              additional_fields = ()

          res= self.sql_connector.session.query(
                                                  PreProjetoModel.NomeProjeto.label('nome'),
                                                  PreProjetoModel.idPreProjeto.label('id'),
                                                  PreProjetoModel.DtInicioDeExecucao.label('data_inicio'),
                                                  PreProjetoModel.DtFinalDeExecucao.label('data_termino'),
                                                  PreProjetoModel.dtAceite.label('data_aceite'),
                                                  PreProjetoModel.DtArquivamento.label('data_arquivamento'),

                                                  MecanismoModel.Descricao.label('mecanismo'),

                                                  *additional_fields

                                                  ).join(MecanismoModel)\
                                                  .order_by(PreProjetoModel.idPreProjeto)

          if nome is not None:
              res = res.filter(PreProjetoModel.NomeProjeto.like('%' + nome + '%'))

          if id is not None:
              res = res.filter(PreProjetoModel.idPreProjeto == id)

          if data_inicio is not None:
              res = res.filter(PreProjetoModel.DtInicioDeExecucao == data_inicio)

          if data_termino is not None:
              res = res.filter(PreProjetoModel.DtFinalDeExecucao == data_termino)

          #total_records = res.count()
          total_records = self.get_count(res)

          res = res.slice(start_row, end_row)

          return res.all(), total_records


    def get_doacoes(self, PRONAC = None, cgccpf = None):

        res = self.sql_connector.session.query(
                                               CaptacaoModel.PRONAC,
                                               CaptacaoModel.CaptacaoReal.label('valor'),
                                               CaptacaoModel.DtRecibo.label('data_recibo'),
                                               #ProjetoModel.PRONAC.label('projeto_PRONAC'),
                                               ProjetoModel.NomeProjeto.label('nome_projeto'),
                                               InteressadoModel.Nome.label('nome_doador'),
                                               CaptacaoModel.CgcCpfMecena.label('cgccpf'),
                                              ).join(ProjetoModel, CaptacaoModel.PRONAC==ProjetoModel.PRONAC)\
                                                .join(InteressadoModel, CaptacaoModel.CgcCpfMecena==InteressadoModel.CgcCpf)\




        if PRONAC is not None:
            res = res.filter(CaptacaoModel.PRONAC == PRONAC)

        if cgccpf is not None:
            res = res.filter(InteressadoModel.CgcCpf.like('%' + cgccpf + '%') )

        return res.all()


    # def get_doacoes(self, cgccpf, limit, offset):

    #     start_row = offset
    #     end_row = offset+limit

    #     res= self.sql_connector.session.query(
    #                                           CaptacaoModel.PRONAC,
    #                                           CaptacaoModel.CaptacaoReal.label('valor'),
    #                                           CaptacaoModel.DtRecibo.label('data_recibo'),
    #                                           ProjetoModel.NomeProjeto.label('nome_projeto'),
    #                                           ) .join(ProjetoModel, CaptacaoModel.PRONAC==ProjetoModel.PRONAC)\
    #                                             .filter(CaptacaoModel.CgcCpfMecena == cgccpf)

    #     total_records = res.count()

    #     #res = res.slice(start_row, end_row)

    #     return res.all(), total_records
