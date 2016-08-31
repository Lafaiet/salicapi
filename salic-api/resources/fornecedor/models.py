from sqlalchemy.sql import text
from ..ModelsBase import ModelsBase
from ..SharedModels import InteressadoModel, ProjetoModel
from ..projeto.models import ProjetoModelObject


class FornecedordorModelObject(ModelsBase):

    def __init__(self):
        super (FornecedordorModelObject,self).__init__()


    def all(self, cgccpf = None, PRONAC = None, nome = None):

        if cgccpf is not None:
            query = text ("""
              SELECT
                   DISTINCT g.CNPJCPF as cgccpf, e.Descricao as nome, Internet.Descricao as email
                    
                   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
                   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
                   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
                   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
                   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
                   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
                   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
                   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente

                   WHERE (g.CNPJCPF LIKE :cgccpf)

              """)

            return self.sql_connector.session.execute(query, {'cgccpf' : '%'+cgccpf+'%'})


        if nome is not None:
            query = text ("""
              SELECT
                   DISTINCT g.CNPJCPF as cgccpf, e.Descricao as nome, Internet.Descricao as email
                    
                   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
                   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
                   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
                   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
                   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
                   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
                   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
                   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente

                   WHERE (e.Descricao LIKE :nome)

              """)

            return self.sql_connector.session.execute(query, {'nome' : '%'+nome+'%'})



        else:
            query = text ("""
              SELECT
                   DISTINCT g.CNPJCPF as cgccpf, e.Descricao as nome, Internet.Descricao as email
                    
                   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
                   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
                   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
                   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
                   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
                   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
                   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
                   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente
                   JOIN SAC.dbo.Projetos AS Projetos ON PlanilhaAprovacao.idPronac = Projetos.IdPRONAC

                   WHERE (Projetos.AnoProjeto + Projetos.Sequencial = :PRONAC)

              """)

            return self.sql_connector.session.execute(query, {'PRONAC' : PRONAC})


class ItemModelObject(ModelsBase):

  def __init__(self):
        super (ItemModelObject,self).__init__()


  def all(self, cgccpf):
      return ProjetoModelObject().payments_listing(cgccpf = cgccpf)

