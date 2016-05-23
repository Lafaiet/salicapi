from connectors.mssql_connector import MSSql_connector
from sqlalchemy import case, func
from ORMClasses import *
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
            res  = self.sql_connector.session.query(AreaDb.Descricao.label('area'))
          return res.all()
        except Exception as e:
          Log.error("Database connection error : " + str(e))
          raise e
    
    def get_segmento(self):
        res  = self.sql_connector.session.query(SegmentoDb.Descricao.label('segmento'))
        return res.all()
    
    def get_resumo(self, PRONAC):
        res  = self.sql_connector.session.query(ProjetoDb.ResumoProjeto.label('resumo')).filter(ProjetoDb.PRONAC == PRONAC)
        return res.one_or_none()
    
    def get_acessibilidade(self, PRONAC):
        res  = self.sql_connector.session.query(PreProjetoDb.Acessibilidade.label('acessibilidade')).join(ProjetoDb).filter(ProjetoDb.PRONAC == PRONAC)
        return res.one_or_none()
    
    def get_objetivos(self, PRONAC):
        res  = self.sql_connector.session.query(PreProjetoDb.Objetivos.label('objetivos')).join(ProjetoDb).filter(ProjetoDb.PRONAC == PRONAC)
        return res.one_or_none()
    
    def get_justificativa(self, PRONAC):
        res  = self.sql_connector.session.query(PreProjetoDb.Justificativa.label('justificativa')).join(ProjetoDb).filter(ProjetoDb.PRONAC == PRONAC)
        return res.one_or_none()
    
    def get_democratizacao_de_acesso(self, PRONAC):
        res  = self.sql_connector.session.query(PreProjetoDb.DemocratizacaoDeAcesso.label('democratizacao_de_acesso')).join(ProjetoDb).filter(ProjetoDb.PRONAC == PRONAC)
        return res.one_or_none()
    
    def get_etapa_de_trabalho(self, PRONAC):
        res  = self.sql_connector.session.query(PreProjetoDb.EtapaDeTrabalho.label('etapa_de_trabalho')).join(ProjetoDb).filter(ProjetoDb.PRONAC == PRONAC)
        return res.one_or_none()
    
    def get_ficha_tecnica(self, PRONAC):
        res  = self.sql_connector.session.query(PreProjetoDb.FichaTecnica.label('FichaTecnica')).join(ProjetoDb).filter(ProjetoDb.PRONAC == PRONAC)
        return res.one_or_none()
    
    def get_providencia(self, PRONAC):
        res  = self.sql_connector.session.query(ProjetoDb.ProvidenciaTomada.label('providencia')).filter(ProjetoDb.PRONAC == PRONAC)
        return res.one_or_none()
    
    def get_proponente(self,  limit, offset, nome = None, cgccpf = None, municipio = None,
                       UF = None, tipo_pessoa = None, all_fields = False):
        
        start_row = offset
        end_row = offset+limit
        
        
        tipo_pessoa_case = case([(InteressadoDb.tipoPessoa=='1', 'fisica'),],
        else_ = 'juridica')

        res= self.sql_connector.session.query( 
                                               InteressadoDb.Nome.label('nome'),
                                               InteressadoDb.Cidade.label('municipio'),
                                               InteressadoDb.Uf.label('UF'),
                                               InteressadoDb.Responsavel.label('responsavel'),
                                               InteressadoDb.CgcCpf.label('cgccpf'),
                                               tipo_pessoa_case.label('tipo_pessoa'),
                                               func.count(ProjetoDb.PRONAC).label('quantidade_projetos'),
                                               ).join(ProjetoDb)\
                                                .group_by(InteressadoDb.Nome,
                                                          InteressadoDb.Cidade,
                                                          InteressadoDb.Uf,
                                                          InteressadoDb.Responsavel,
                                                          InteressadoDb.CgcCpf,
                                                          tipo_pessoa_case,
                                                  )\
                                                .order_by(InteressadoDb.CgcCpf)

        
        if cgccpf is not None:
            res = res.filter(InteressadoDb.CgcCpf.like('%' + cgccpf + '%'))
            
        if nome is not None:
            res = res.filter(InteressadoDb.Nome.like('%' + nome + '%'))
            
        if UF is not None:
            res = res.filter(InteressadoDb.Uf == UF)
                
        if municipio is not None:
            res = res.filter(InteressadoDb.Cidade == municipio)
        
        if tipo_pessoa is not None:
            if tipo_pessoa == 'fisica':
                tipo_pessoa = '1'
            else:
                tipo_pessoa = '2'
                
            res = res.filter(InteressadoDb.tipoPessoa == tipo_pessoa )
        
        total_records = res.count()
        
        res = res.slice(start_row, end_row)
        
        return res.all(), total_records
    
    
    def get_incentivador(self,  limit, offset, nome = None, cgccpf = None, municipio = None, UF = None, tipo_pessoa = None):
        
        start_row = offset
        end_row = offset+limit
        
        tipo_pessoa_case = case([(InteressadoDb.tipoPessoa=='1', 'fisica'),],
        else_ = 'juridica')
        
        res= self.sql_connector.session.query( 
                                               InteressadoDb.Nome.label('nome'),
                                               InteressadoDb.Cidade.label('municipio'),
                                               InteressadoDb.Uf.label('UF'),
                                               InteressadoDb.Responsavel.label('responsavel'),
                                               InteressadoDb.CgcCpf.label('cgccpf'),
                                               func.sum(CaptacaoDb.CaptacaoReal).label('total_doado'),
                                               tipo_pessoa_case.label('tipo_pessoa'),
                                               ).join(CaptacaoDb)\
                                               .group_by(InteressadoDb.Nome,
                                                         InteressadoDb.Cidade,
                                                         InteressadoDb.Uf,
                                                         InteressadoDb.Responsavel,
                                                         InteressadoDb.CgcCpf,
                                                         tipo_pessoa_case
                                                          )\
                                               .order_by(InteressadoDb.CgcCpf)
        
        if cgccpf is not None:
            res = res.filter(InteressadoDb.CgcCpf.like('%' + cgccpf + '%') )
            
        if nome is not None:
            res = res.filter(InteressadoDb.Nome.like('%' + nome + '%'))
            
        if UF is not None:
            res = res.filter(InteressadoDb.Uf == UF)
                
        if municipio is not None:
            res = res.filter(InteressadoDb.Cidade == municipio)
        
        if tipo_pessoa is not None:
            if tipo_pessoa == 'fisica':
                tipo_pessoa = '1'
            else:
                tipo_pessoa = '2'
                
            res = res.filter(InteressadoDb.tipoPessoa == tipo_pessoa )
        
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
                             PreProjetoDb.Acessibilidade.label('acessibilidade'),
                             PreProjetoDb.Objetivos.label('objetivos'),
                             PreProjetoDb.Justificativa.label('justificativa'),
                             PreProjetoDb.DemocratizacaoDeAcesso.label('democratizacao'),
                             PreProjetoDb.EtapaDeTrabalho.label('etapa'),
                             PreProjetoDb.FichaTecnica.label('ficha_tecnica'),
                             PreProjetoDb.ResumoDoProjeto.label('resumo'),
                             PreProjetoDb.Sinopse.label('sinopse'),
                             PreProjetoDb.ImpactoAmbiental.label('impacto_ambiental'),
                             PreProjetoDb.EspecificacaoTecnica.label('especificacao_tecnica'),
                             PreProjetoDb.EstrategiadeExecucao.label('estrategia_execucao'),

                             ProjetoDb.ProvidenciaTomada.label('providencia'),
                             )
        else:
            additional_fields = ()
        
        
        valor_proposta_case = case([(ProjetoDb.IdPRONAC != None, func.sac.dbo.fnValorDaProposta(ProjetoDb.IdPRONAC)),],
        else_ = func.sac.dbo.fnValorSolicitado(ProjetoDb.AnoProjeto, ProjetoDb.Sequencial))
        
        valor_aprovado_case = case([(ProjetoDb.Mecanismo == '2' or ProjetoDb.Mecanismo == '6', func.sac.dbo.fnValorAprovadoConvenio(ProjetoDb.AnoProjeto,ProjetoDb.Sequencial)),],
        else_ = func.sac.dbo.fnValorAprovado(ProjetoDb.AnoProjeto,ProjetoDb.Sequencial))

        valor_projeto_case = case([(ProjetoDb.Mecanismo =='2' or ProjetoDb.Mecanismo =='6', func.sac.dbo.fnValorAprovadoConvenio(ProjetoDb.AnoProjeto,ProjetoDb.Sequencial)),],
        else_ = func.sac.dbo.fnValorAprovado(ProjetoDb.AnoProjeto,ProjetoDb.Sequencial) + func.sac.dbo.fnOutrasFontes(ProjetoDb.IdPRONAC))
        
        enquadramento_case = case([(EnquadramentoDb.Enquadramento == '1', 'Artigo 26'),
                                   (EnquadramentoDb.Enquadramento == '2', 'Artigo 18')
                                   ],
        else_ = 'Nao enquadrado')

        ano_case = case([(ProjetoDb.Mecanismo =='2' or ProjetoDb.Mecanismo =='6', func.sac.dbo.fnValorAprovadoConvenio(ProjetoDb.AnoProjeto,ProjetoDb.Sequencial)),],
        else_ = func.sac.dbo.fnValorAprovado(ProjetoDb.AnoProjeto,ProjetoDb.Sequencial))
        
        with Timer(action = 'Database query for get_projeto_list method', verbose = True):
          res= self.sql_connector.session.query( 
                                                  ProjetoDb.NomeProjeto.label('nome'),
                                                  ProjetoDb.PRONAC,
                                                  ProjetoDb.AnoProjeto.label('ano_projeto'),
                                                  ProjetoDb.UfProjeto.label('UF'),
                                                  InteressadoDb.Cidade.label('municipio'),
                                                  ProjetoDb.DtInicioExecucao.label('data_inicio'),
                                                  ProjetoDb.DtFimExecucao.label('data_termino'),
                                  
                                                  AreaDb.Descricao.label('area'),
                                                  SegmentoDb.Descricao.label('segmento'),
                                                  SituacaoDb.Descricao.label('situacao'),
                                                  InteressadoDb.Nome.label('proponente'),
                                                  InteressadoDb.CgcCpf.label('cgccpf'),
                                                  MecanismoDb.Descricao.label('mecanismo'),
                                                  
                                                  func.sac.dbo.fnValorSolicitado(ProjetoDb.AnoProjeto, ProjetoDb.Sequencial).label('valor_solicitado'),
                                                  func.sac.dbo.fnOutrasFontes(ProjetoDb.IdPRONAC).label('outras_fontes'),
                                                  func.sac.dbo.fnCustoProjeto (ProjetoDb.AnoProjeto, ProjetoDb.Sequencial).label('valor_captado'),
                                                  valor_proposta_case.label('valor_proposta'),
                                                  valor_aprovado_case.label('valor_aprovado'),
                                                  valor_projeto_case.label('valor_projeto'),
                                                  
                                                  enquadramento_case.label('enquadramento'),
                                                  
                                                  *additional_fields
                                                  
                                                  ).join(AreaDb)\
                                                  .join(SegmentoDb)\
                                                  .join(SituacaoDb)\
                                                  .join(InteressadoDb)\
                                                  .join(PreProjetoDb)\
                                                  .join(MecanismoDb)\
                                                  .outerjoin(EnquadramentoDb, EnquadramentoDb.IdPRONAC ==  ProjetoDb.IdPRONAC)\
                                                  .order_by(ProjetoDb.IdPRONAC)
                                                
        if PRONAC is not None:
            res = res.filter(ProjetoDb.PRONAC == PRONAC)
        
        if area is not None:
            res = res.filter(AreaDb.Descricao == area)
        
        if segmento is not None:
            res = res.filter(SegmentoDb.Descricao == segmento)
        
        if proponente is not None:
            res = res.filter(InteressadoDb.Nome.like('%' + proponente + '%'))
            
        if cgccpf is not None:
            res = res.filter(InteressadoDb.CgcCpf.like('%' + cgccpf + '%') )
            
        if nome is not None:
            res = res.filter(ProjetoDb.NomeProjeto.like('%' + nome + '%'))
            
        if UF is not None:
            res = res.filter(InteressadoDb.Uf == UF)

        if municipio is not None:
            res = res.filter(InteressadoDb.Cidade == municipio)
        
        if data_inicio is not None:
            res = res.filter(ProjetoDb.DtInicioExecucao == data_inicio)
            
        if data_termino is not None:
            res = res.filter(ProjetoDb.DtFimExecucao == data_termino)

        if ano_projeto is not None:
            res = res.filter(ProjetoDb.AnoProjeto == ano_projeto)

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
                               PreProjetoDb.Acessibilidade.label('acessibilidade'),
                               PreProjetoDb.Objetivos.label('objetivos'),
                               PreProjetoDb.Justificativa.label('justificativa'),
                               PreProjetoDb.DemocratizacaoDeAcesso.label('democratizacao'),
                               PreProjetoDb.EtapaDeTrabalho.label('etapa'),
                               PreProjetoDb.FichaTecnica.label('ficha_tecnica'),
                               PreProjetoDb.ResumoDoProjeto.label('resumo'),
                               PreProjetoDb.Sinopse.label('sinopse'),
                               PreProjetoDb.ImpactoAmbiental.label('impacto_ambiental'),
                               PreProjetoDb.EspecificacaoTecnica.label('especificacao_tecnica'),
                               PreProjetoDb.EstrategiadeExecucao.label('estrategia_execucao'),
                               )
          else:
              additional_fields = ()
          
          res= self.sql_connector.session.query( 
                                                  PreProjetoDb.NomeProjeto.label('nome'),
                                                  PreProjetoDb.idPreProjeto.label('id'),
                                                  PreProjetoDb.DtInicioDeExecucao.label('data_inicio'),
                                                  PreProjetoDb.DtFinalDeExecucao.label('data_termino'),
                                                  PreProjetoDb.dtAceite.label('data_aceite'),
                                                  PreProjetoDb.DtArquivamento.label('data_arquivamento'),

                                                  MecanismoDb.Descricao.label('mecanismo'),
                                                  
                                                  *additional_fields
                                                  
                                                  ).join(MecanismoDb)\
                                                  .order_by(PreProjetoDb.idPreProjeto)
              
          if nome is not None:
              res = res.filter(PreProjetoDb.NomeProjeto.like('%' + nome + '%'))

          if id is not None:
              res = res.filter(PreProjetoDb.idPreProjeto == id)
          
          if data_inicio is not None:
              res = res.filter(PreProjetoDb.DtInicioDeExecucao == data_inicio)
              
          if data_termino is not None:
              res = res.filter(PreProjetoDb.DtFinalDeExecucao == data_termino)
          
          #total_records = res.count()
          total_records = self.get_count(res)

          res = res.slice(start_row, end_row)
          
          return res.all(), total_records


    def get_doacoes(self, PRONAC = None, cgccpf = None):
        
        res = self.sql_connector.session.query(
                                               CaptacaoDb.PRONAC,
                                               CaptacaoDb.CaptacaoReal.label('valor'), 
                                               CaptacaoDb.DtRecibo.label('data_recibo'),
                                               #ProjetoDb.PRONAC.label('projeto_PRONAC'),
                                               ProjetoDb.NomeProjeto.label('nome_projeto'),
                                               InteressadoDb.Nome.label('nome_doador'),
                                               CaptacaoDb.CgcCpfMecena.label('cgccpf'),
                                              ).join(ProjetoDb, CaptacaoDb.PRONAC==ProjetoDb.PRONAC)\
                                                .join(InteressadoDb, CaptacaoDb.CgcCpfMecena==InteressadoDb.CgcCpf)\
                                                
                                              


        if PRONAC is not None:
            res = res.filter(CaptacaoDb.PRONAC == PRONAC)   
        
        if cgccpf is not None:
            res = res.filter(InteressadoDb.CgcCpf.like('%' + cgccpf + '%') )              

        return res.all()


    # def get_doacoes(self, cgccpf, limit, offset):
        
    #     start_row = offset
    #     end_row = offset+limit
        
    #     res= self.sql_connector.session.query( 
    #                                           CaptacaoDb.PRONAC,
    #                                           CaptacaoDb.CaptacaoReal.label('valor'),
    #                                           CaptacaoDb.DtRecibo.label('data_recibo'),
    #                                           ProjetoDb.NomeProjeto.label('nome_projeto'),
    #                                           ) .join(ProjetoDb, CaptacaoDb.PRONAC==ProjetoDb.PRONAC)\
    #                                             .filter(CaptacaoDb.CgcCpfMecena == cgccpf)
                        
    #     total_records = res.count()
        
    #     #res = res.slice(start_row, end_row)
        
    #     return res.all(), total_records
        
