from sqlalchemy import case, func

from ..ModelsBase import ModelsBase
from ..SharedModels import InteressadoModel, CaptacaoModel, ProjetoModel


class IncentivadorModelObject(ModelsBase):

    def __init__(self):
        super (IncentivadorModelObject,self).__init__()



    def all(self,  limit, offset, nome = None, cgccpf = None, municipio = None, UF = None, tipo_pessoa = None):

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



class DoacaoModelObject(ModelsBase):

    def __init__(self):
        super (DoacaoModelObject,self).__init__()



    def all(self, cgccpf = None):

        res = self.sql_connector.session.query(
                                               CaptacaoModel.PRONAC,
                                               CaptacaoModel.CaptacaoReal.label('valor'),
                                               CaptacaoModel.DtRecibo.label('data_recibo'),
                                               ProjetoModel.NomeProjeto.label('nome_projeto'),
                                              ).join(ProjetoModel, CaptacaoModel.PRONAC==ProjetoModel.PRONAC)\
                                                .join(InteressadoModel, CaptacaoModel.CgcCpfMecena==InteressadoModel.CgcCpf)\




        if cgccpf is not None:
            res = res.filter(InteressadoModel.CgcCpf.like('%' + cgccpf + '%') )

        return res.all()
