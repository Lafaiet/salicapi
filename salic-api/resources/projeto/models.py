# -*- coding: utf-8 -*-

from sqlalchemy import case, func, and_
from sqlalchemy.orm import aliased
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import asc, desc

from ..ModelsBase import ModelsBase
from ..SharedModels import AreaModel, SegmentoModel
from ..SharedModels import (ProjetoModel, InteressadoModel, MecanismoModel,
                            SituacaoModel, EnquadramentoModel,
                            PreProjetoModel, CaptacaoModel, CertidoesNegativasModel,
                            VerificacaoModel, PlanoDivulgacaoModel, PlanoDistribuicaoModel,
                            ProdutoModel, AreaModel, SegmentoModel
                            )


import sys
sys.path.append('../../')
from utils.Timer import Timer
from utils.Log import Log



class ProjetoModelObject(ModelsBase):

    def __init__(self):
        super (ProjetoModelObject, self).__init__()

    def attached_documents(self, idPronac ):
        query = text("""SAC.dbo.paDocumentos :idPronac""")
        return self.sql_connector.session.execute(query, {'idPronac' : idPronac})

    def attached_brands(self, idPronac):

        query = text("""
                    SELECT a.idArquivo as id_arquivo, a.nmArquivo as nome_arquivo, a.dtEnvio as data_envio, d.idDocumento as id_documento, CAST(dsDocumento AS TEXT) AS descricao
                           
                    FROM BDCORPORATIVO.scCorp.tbArquivoImagem AS ai
                    INNER JOIN BDCORPORATIVO.scCorp.tbArquivo AS a ON ai.idArquivo = a.idArquivo
                    INNER JOIN BDCORPORATIVO.scCorp.tbDocumento AS d ON a.idArquivo = d.idArquivo
                    INNER JOIN BDCORPORATIVO.scCorp.tbDocumentoProjeto AS dp ON dp.idDocumento = d.idDocumento
                    INNER JOIN SAC.dbo.Projetos AS p ON dp.idPronac = p.IdPRONAC WHERE (dp.idTipoDocumento = 1) AND (p.idPronac = :IdPRONAC)
        """)
        return self.sql_connector.session.execute(query, {'IdPRONAC' : idPronac})

    def postpone_request(self, idPronac):

        query = text("""
                    SELECT a.DtPedido as data_pedido, a.DtInicio as data_inicio, a.DtFinal as data_final, a.Observacao as observacao, a.Atendimento as atendimento,
                        CASE
                            WHEN Atendimento = 'A'
                                THEN 'Em analise'
                            WHEN Atendimento = 'N'
                                THEN 'Deferido'
                            WHEN Atendimento = 'I'
                                THEN 'Indeferido'
                            WHEN Atendimento = 'S'
                                THEN 'Processado'
                            END as estado
                        , b.usu_nome AS usuario FROM prorrogacao AS a
                        LEFT JOIN TABELAS.dbo.Usuarios AS b ON a.Logon = b.usu_codigo WHERE (idPronac = :IdPRONAC)
        """)

        return self.sql_connector.session.execute(query, {'IdPRONAC' : idPronac})


    def payments_listing(self, idPronac = None, cgccpf = None):
        #Relação de pagamentos

        if idPronac != None:

            query = text("""
                        SELECT
                                d.Descricao as nome,
                                b.idComprovantePagamento as id_comprovante_pagamento,
                                a.idPlanilhaAprovacao as id_planilha_aprovacao,
                                g.CNPJCPF as cgccpf,
                                e.Descricao as nome_fornecedor,
                                b.DtPagamento as data_aprovacao,
                                CASE tpDocumento
                                    WHEN 1 THEN ('Boleto Bancario')
                                    WHEN 2 THEN ('Cupom Fiscal')
                                    WHEN 3 THEN ('Guia de Recolhimento')
                                    WHEN 4 THEN ('Nota Fiscal/Fatura')
                                    WHEN 5 THEN ('Recibo de Pagamento')
                                    WHEN 6 THEN ('RPA')
                                    ELSE ''
                                END as tipo_documento,
                                b.nrComprovante as nr_comprovante,
                                b.dtEmissao as data_pagamento,
                                CASE
                                  WHEN b.tpFormaDePagamento = '1'
                                     THEN 'Cheque'
                                  WHEN b.tpFormaDePagamento = '2'
                                     THEN 'Transferencia Bancaria'  WHEN b.tpFormaDePagamento = '3'
                                     THEN 'Saque/Dinheiro'
                                     ELSE ''
                                END as tipo_forma_pagamento,
                                b.nrDocumentoDePagamento nr_documento_pagamento,
                                a.vlComprovado as valor_pagamento,
                                b.idArquivo as id_arquivo,
                                b.dsJustificativa as justificativa,
                                f.nmArquivo as nm_arquivo FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
                                INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
                                LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS c ON a.idPlanilhaAprovacao = c.idPlanilhaAprovacao
                                LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON c.idPlanilhaItem = d.idPlanilhaItens
                                LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
                                LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
                                LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente WHERE (c.idPronac = :idPronac)
                                """
                                )
            return self.sql_connector.session.execute(query, {'idPronac' : idPronac})

        else:
            query = text("""
                        SELECT
                                d.Descricao as nome,
                                b.idComprovantePagamento as id_comprovante_pagamento,
                                a.idPlanilhaAprovacao as id_planilha_aprovacao,
                                g.CNPJCPF as cgccpf,
                                e.Descricao as nome_fornecedor,
                                b.DtPagamento as data_aprovacao,
                                Projetos.AnoProjeto + Projetos.Sequencial as PRONAC,
                                CASE tpDocumento
                                    WHEN 1 THEN ('Boleto Bancario')
                                    WHEN 2 THEN ('Cupom Fiscal')
                                    WHEN 3 THEN ('Guia de Recolhimento')
                                    WHEN 4 THEN ('Nota Fiscal/Fatura')
                                    WHEN 5 THEN ('Recibo de Pagamento')
                                    WHEN 6 THEN ('RPA')
                                    ELSE ''
                                END as tipo_documento,
                                b.nrComprovante as nr_comprovante,
                                b.dtEmissao as data_pagamento,
                                CASE
                                  WHEN b.tpFormaDePagamento = '1'
                                     THEN 'Cheque'
                                  WHEN b.tpFormaDePagamento = '2'
                                     THEN 'Transferencia Bancaria'  WHEN b.tpFormaDePagamento = '3'
                                     THEN 'Saque/Dinheiro'
                                     ELSE ''
                                END as tipo_forma_pagamento,
                                b.nrDocumentoDePagamento nr_documento_pagamento,
                                a.vlComprovado as valor_pagamento,
                                b.idArquivo as id_arquivo,
                                b.dsJustificativa as justificativa,
                                f.nmArquivo as nm_arquivo FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
                                INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
                                LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS c ON a.idPlanilhaAprovacao = c.idPlanilhaAprovacao
                                LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON c.idPlanilhaItem = d.idPlanilhaItens
                                LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
                                LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
                                JOIN SAC.dbo.Projetos AS Projetos ON c.idPronac = Projetos.IdPRONAC
                                LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente WHERE (g.CNPJCPF LIKE :cgccpf)
                                """
                                )

            return self.sql_connector.session.execute(query, {'cgccpf' : '%'+cgccpf+'%'})




    def taxing_report(self, idPronac):
        # Relatório fisco

        query = text("""
                    SELECT
                    f.idPlanilhaEtapa,
                    f.Descricao AS Etapa,
                    d.Descricao AS Item,
                    g.Descricao AS Unidade,
                    (c.qtItem*nrOcorrencia) AS qteProgramada,
                    (c.qtItem*nrOcorrencia*c.vlUnitario) AS vlProgramado,
                    ((sum(b.vlComprovacao) / (c.qtItem*nrOcorrencia*c.vlUnitario)) * 100) AS PercExecutado,
                    (sum(b.vlComprovacao)) AS vlExecutado,
                    (100 - (sum(b.vlComprovacao) / (c.qtItem*nrOcorrencia*c.vlUnitario)) * 100) AS PercAExecutar
                 FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
                 INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
                 INNER JOIN SAC.dbo.tbPlanilhaAprovacao AS c ON a.idPlanilhaAprovacao = c.idPlanilhaAprovacao
                 INNER JOIN SAC.dbo.tbPlanilhaItens AS d ON c.idPlanilhaItem = d.idPlanilhaItens
                 INNER JOIN SAC.dbo.tbPlanilhaEtapa AS f ON c.idEtapa = f.idPlanilhaEtapa
                 INNER JOIN SAC.dbo.tbPlanilhaUnidade AS g ON c.idUnidade= g.idUnidade WHERE (c.idPronac = :IdPRONAC) GROUP BY c.idPronac,
                    f.Descricao,
                    d.Descricao,
                    g.Descricao,
                    c.qtItem,
                    nrOcorrencia,
                    c.vlUnitario,
                    f.idPlanilhaEtapa
                    """
                    )

        return self.sql_connector.session.execute(query, {'IdPRONAC' : idPronac})


    def goods_capital_listing(self, idPronac):
        #Relação de bens de capital

        query = text("""
                    SELECT
                    CASE
                        WHEN tpDocumento = 1 THEN 'Boleto Bancario'
                        WHEN tpDocumento = 2 THEN 'Cupom Fiscal'
                        WHEN tpDocumento = 3 THEN 'Nota Fiscal / Fatura'
                        WHEN tpDocumento = 4 THEN 'Recibo de Pagamento'
                        WHEN tpDocumento = 5 THEN 'RPA'
                    END as Titulo,
                    b.nrComprovante,
                    d.Descricao as Item,
                    DtEmissao as dtPagamento,
                    dsItemDeCusto Especificacao,
                    dsMarca as Marca,
                    dsFabricante as Fabricante,
                    (c.qtItem*nrOcorrencia) as Qtde,
                    c.vlUnitario,
                    (c.qtItem*nrOcorrencia*c.vlUnitario) as vlTotal
                 FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
                 INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
                 INNER JOIN SAC.dbo.tbPlanilhaAprovacao AS c ON a.idPlanilhaAprovacao = c.idPlanilhaAprovacao
                 INNER JOIN SAC.dbo.tbPlanilhaItens AS d ON c.idPlanilhaItem = d.idPlanilhaItens
                 INNER JOIN BDCORPORATIVO.scSAC.tbItemCusto AS e ON e.idPlanilhaAprovacao = c.idPlanilhaAprovacao
                 WHERE (c.idPronac = :IdPRONAC)
        """)

        return self.sql_connector.session.execute(query, {'IdPRONAC' : idPronac})


    def all(self, limit, offset, PRONAC = None, nome = None, proponente = None,
                          cgccpf = None, area = None, segmento = None,
                          UF = None, municipio = None, data_inicio = None,
                          data_inicio_min = None, data_inicio_max = None,
                          data_termino = None, data_termino_min = None,
                          data_termino_max = None, ano_projeto = None, sort_field = None, sort_order = None):



        text_fields = (
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

        sort_mapping_fields = { 'valor_solicitado' : func.sac.dbo.fnValorSolicitado(ProjetoModel.AnoProjeto, ProjetoModel.Sequencial),
                                'PRONAC' : ProjetoModel.PRONAC,
                                'outras_fontes' : func.sac.dbo.fnOutrasFontes(ProjetoModel.IdPRONAC),
                                'valor_captado' : func.sac.dbo.fnCustoProjeto (ProjetoModel.AnoProjeto, ProjetoModel.Sequencial),
                                'valor_proposta' : valor_proposta_case,
                                'valor_aprovado' : valor_aprovado_case,
                                'valor_projeto' :  valor_projeto_case,
                                'ano_projeto' : ProjetoModel.AnoProjeto,
                                'data_inicio' : ProjetoModel.DtInicioExecucao,
                                'data_termino' : ProjetoModel.DtFimExecucao,
        }

        if sort_field == None:
            sort_field = 'ano_projeto'
            sort_order = 'desc'

        sort_field = sort_mapping_fields[sort_field]

        with Timer(action = 'Database query for get_projeto_list method', verbose = True):
          res = self.sql_connector.session.query(
                                                  ProjetoModel.NomeProjeto.label('nome'),
                                                  ProjetoModel.PRONAC.label('PRONAC'),
                                                  ProjetoModel.AnoProjeto.label('ano_projeto'),
                                                  ProjetoModel.UfProjeto.label('UF'),
                                                  InteressadoModel.Cidade.label('municipio'),
                                                  ProjetoModel.DtInicioExecucao.label('data_inicio'),
                                                  ProjetoModel.DtFimExecucao.label('data_termino'),
                                                  ProjetoModel.IdPRONAC,

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

                                                  *text_fields

                                                  ).join(AreaModel)\
                                                  .join(SegmentoModel)\
                                                  .join(SituacaoModel)\
                                                  .join(InteressadoModel)\
                                                  .join(PreProjetoModel)\
                                                  .join(MecanismoModel)\
                                                  .outerjoin(EnquadramentoModel, EnquadramentoModel.IdPRONAC ==  ProjetoModel.IdPRONAC)
                                                


        if PRONAC is not None:
            res = res.filter(ProjetoModel.PRONAC == PRONAC)

        if area is not None:
            res = res.filter(AreaModel.Codigo == area)

        if segmento is not None:
            res = res.filter(SegmentoModel.Codigo == segmento)

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

        # order by descending
        if sort_order == 'desc':
            res = res.order_by(desc(sort_field))
        #order by ascending
        else:
            res = res.order_by(sort_field)

        #res = res.order_by("AnoProjeto")

        total_records = self.count(res)

        # with Timer(action = 'Projects count() slow ', verbose = True):
        #   total_records = res.count()
        #   #Log.debug("total : "+str(total_records))

        #with Timer(action = 'Projects slice()', verbose = True):
          # res = res.slice(start_row, end_row)
        res = res.limit(limit).offset(offset)

        return res.all(), total_records



class CaptacaoModelObject(ModelsBase):

    def all(self, PRONAC):

        res = self.sql_connector.session.query(
                                               CaptacaoModel.PRONAC,
                                               CaptacaoModel.CaptacaoReal.label('valor'),
                                               CaptacaoModel.DtRecibo.label('data_recibo'),
                                               ProjetoModel.NomeProjeto.label('nome_projeto'),
                                               CaptacaoModel.CgcCpfMecena.label('cgccpf'),
                                               InteressadoModel.Nome.label('nome_doador'),
                                              ).join(ProjetoModel, CaptacaoModel.PRONAC==ProjetoModel.PRONAC)\
                                                .join(InteressadoModel, CaptacaoModel.CgcCpfMecena==InteressadoModel.CgcCpf)\


        if PRONAC is not None:
            res = res.filter(CaptacaoModel.PRONAC == PRONAC)

        return res.all()



class AreaModelObject(ModelsBase):

    def __init__(self):
        super (AreaModelObject,self).__init__()

    def all(self):
        res  = self.sql_connector.session.query(AreaModel.Descricao.label('nome'), AreaModel.Codigo.label('codigo'))
        return res.all()



class SegmentoModelObject(ModelsBase):

    def __init__(self):
        super (SegmentoModelObject,self).__init__()


    def all(self):
        res  = self.sql_connector.session.query(SegmentoModel.Descricao.label('nome'), SegmentoModel.Codigo.label('codigo'))
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

class DivulgacaoModelObject(ModelsBase):

    V1 = aliased(VerificacaoModel)
    V2 = aliased(VerificacaoModel)


    def __init__(self):
        super (DivulgacaoModelObject,self).__init__()


    def all(self, IdPRONAC):

        stmt = text(
                    """
                        SELECT v1.Descricao as peca,v2.Descricao as veiculo
                        FROM sac.dbo.PlanoDeDivulgacao d
                        INNEr JOIN sac.dbo.Projetos p on (d.idProjeto = p.idProjeto)
                        INNER JOIN sac.dbo.Verificacao v1 on (d.idPeca = v1.idVerificacao)
                        INNER JOIN sac.dbo.Verificacao v2 on (d.idVeiculo = v2.idVerificacao)
                        WHERE p.IdPRONAC=:IdPRONAC AND d.stPlanoDivulgacao = 1
                    """
                    )

        return self.sql_connector.session.execute(stmt, {'IdPRONAC' : IdPRONAC})


class DescolamentoModelObject(ModelsBase):

    def __init__(self):
        super (DescolamentoModelObject,self).__init__()

    def all(self, IdPRONAC):

        stmt = text(
                    """
                        SELECT
                            idDeslocamento,
                            d.idProjeto,
                            p.Descricao as PaisOrigem,
                            u.Descricao as UFOrigem,
                            m.Descricao as MunicipioOrigem,
                            p2.Descricao as PaisDestino,
                            u2.Descricao as UFDestino,
                            m2.Descricao as MunicipioDestino,
                            Qtde
                FROM
                   Sac.dbo.tbDeslocamento d
                INNER JOIN Sac.dbo.Projetos y on (d.idProjeto = y.idProjeto)
                INNER JOIN Agentes..Pais p on (d.idPaisOrigem = p.idPais)
                INNER JOIN Agentes..uf u on (d.idUFOrigem = u.iduf)
                INNER JOIN Agentes..Municipios m on (d.idMunicipioOrigem = m.idMunicipioIBGE)
                INNER JOIN Agentes..Pais p2 on (d.idPaisDestino = p2.idPais)
                INNER JOIN Agentes..uf u2 on (d.idUFDestino = u2.iduf)
                INNER JOIN Agentes..Municipios m2 on (d.idMunicipioDestino = m2.idMunicipioIBGE)
                WHERE y.idPRONAC = :IdPRONAC
                    """
        )

        return self.sql_connector.session.execute(stmt, {'IdPRONAC' : IdPRONAC})

class DistribuicaoModelObject(ModelsBase):

    def __init__(self):
        super (DistribuicaoModelObject,self).__init__()


    def all(self, IdPRONAC):

        res  = self.sql_connector.session.query( PlanoDistribuicaoModel.idPlanoDistribuicao,
                                                 PlanoDistribuicaoModel.QtdeVendaNormal,
                                                 PlanoDistribuicaoModel.QtdeVendaPromocional,
                                                 PlanoDistribuicaoModel.PrecoUnitarioNormal,
                                                 PlanoDistribuicaoModel.PrecoUnitarioPromocional,
                                                 PlanoDistribuicaoModel.QtdeOutros,
                                                 PlanoDistribuicaoModel.QtdeProponente,
                                                 PlanoDistribuicaoModel.QtdeProduzida,
                                                 PlanoDistribuicaoModel.QtdePatrocinador,

                                                 AreaModel.Descricao.label('area'),
                                                 SegmentoModel.Descricao.label('segmento'),

                                                 ProdutoModel.Descricao.label('produto'),
                                                 VerificacaoModel.Descricao.label('posicao_logo'),
                                                 ProjetoModel.Localizacao,
        ).join(ProjetoModel)\
         .join(ProdutoModel)\
         .join(AreaModel, AreaModel.Codigo == PlanoDistribuicaoModel.Area)\
         .join(SegmentoModel, SegmentoModel.Codigo == PlanoDistribuicaoModel.Segmento)\
         .join(VerificacaoModel)\

        res  = res.filter(and_(ProjetoModel.IdPRONAC == IdPRONAC, PlanoDistribuicaoModel.stPlanoDistribuicaoProduto == 1))

        return res.all()


class AdequacoesPedidoModelObject(ModelsBase):

    def __init__(self):
        super (AdequacoesPedidoModelObject,self).__init__()

    def all(self, IdPRONAC):

        stmt = text(
                    """
                    SELECT
                a.idReadequacao,
                a.idPronac,
                a.dtSolicitacao,
                CAST(a.dsSolicitacao AS TEXT) AS dsSolicitacao,
                CAST(a.dsJustificativa AS TEXT) AS dsJustificativa,
                a.idSolicitante,
                a.idAvaliador,
                a.dtAvaliador,
                CAST(a.dsAvaliacao AS TEXT) AS dsAvaliacao,
                a.idTipoReadequacao,
                CAST(c.dsReadequacao AS TEXT) AS dsReadequacao,
                a.stAtendimento,
                a.siEncaminhamento,
                CAST(b.dsEncaminhamento AS TEXT) AS dsEncaminhamento,
                a.stEstado,
                e.idArquivo,
                e.nmArquivo
             FROM SAC.dbo.tbReadequacao AS a
             INNER JOIN SAC.dbo.tbTipoEncaminhamento AS b ON a.siEncaminhamento = b.idTipoEncaminhamento INNER JOIN SAC.dbo.tbTipoReadequacao AS c ON c.idTipoReadequacao = a.idTipoReadequacao
             LEFT JOIN BDCORPORATIVO.scCorp.tbDocumento AS d ON d.idDocumento = a.idDocumento
             LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS e ON e.idArquivo = d.idArquivo WHERE (a.idPronac = :IdPRONAC) AND (a.siEncaminhamento <> 12)
                    """
        )

        return self.sql_connector.session.execute(stmt, {'IdPRONAC' : IdPRONAC})

class AdequacoesParecerModelObject(ModelsBase):

    def __init__(self):
        super (AdequacoesParecerModelObject,self).__init__()

    def all(self, IdPRONAC):

        stmt = text(
                    """
                    SELECT
                                    a.idReadequacao,
                                    a.idPronac,
                                    a.dtSolicitacao,
                                    CAST(a.dsSolicitacao AS TEXT) AS dsSolicitacao,
                                    CAST(a.dsJustificativa AS TEXT) AS dsJustificativa,
                                    a.idSolicitante,
                                    a.idAvaliador,
                                    a.dtAvaliador,
                                    CAST(a.dsAvaliacao AS TEXT) AS dsAvaliacao,
                                    a.idTipoReadequacao,
                                    CAST(c.dsReadequacao AS TEXT) AS dsReadequacao,
                                    a.stAtendimento,
                                    a.siEncaminhamento,
                                    CAST(b.dsEncaminhamento AS TEXT) AS dsEncaminhamento,
                                    a.stEstado,
                                    e.idArquivo,
                                    e.nmArquivo
                                 FROM tbReadequacao AS a
                     INNER JOIN SAC.dbo.tbTipoEncaminhamento AS b ON a.siEncaminhamento = b.idTipoEncaminhamento
                     INNER JOIN SAC.dbo.tbTipoReadequacao AS c ON c.idTipoReadequacao = a.idTipoReadequacao
                     LEFT JOIN BDCORPORATIVO.scCorp.tbDocumento AS d ON d.idDocumento = a.idDocumento
                     LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS e ON e.idArquivo = d.idArquivo WHERE (a.idPronac = :IdPRONAC) AND (a.siEncaminhamento <> 12)
                    """
        )

        return self.sql_connector.session.execute(stmt, {'IdPRONAC' : IdPRONAC})
