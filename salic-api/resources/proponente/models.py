from sqlalchemy import case, func

from sqlalchemy.sql.expression import asc, desc

from ..ModelsBase import ModelsBase
from ..SharedModels import InteressadoModel, ProjetoModel




class ProponenteModelObject(ModelsBase):

    def __init__(self):
        super (ProponenteModelObject,self).__init__()


    def all(self,  limit, offset, nome = None, cgccpf = None, municipio = None,
                       UF = None, tipo_pessoa = None, sort_field = None, sort_order = None):

        start_row = offset
        end_row = offset+limit

        sort_mapping_fields = {'cgccpf' : InteressadoModel.CgcCpf,
         'total_captado' : func.sum(func.sac.dbo.fnCustoProjeto (ProjetoModel.AnoProjeto, ProjetoModel.Sequencial))}

        if sort_field == None:
            sort_field = 'cgccpf'

        sort_field = sort_mapping_fields[sort_field]


        tipo_pessoa_case = case([(InteressadoModel.tipoPessoa=='1', 'fisica'),],
        else_ = 'juridica')

        res= self.sql_connector.session.query(
                                               func.sum(func.sac.dbo.fnCustoProjeto (ProjetoModel.AnoProjeto, ProjetoModel.Sequencial)).label('total_captado'),
                                               InteressadoModel.Nome.label('nome'),
                                               InteressadoModel.Cidade.label('municipio'),
                                               InteressadoModel.Uf.label('UF'),
                                               InteressadoModel.Responsavel.label('responsavel'),
                                               InteressadoModel.CgcCpf.label('cgccpf'),
                                               tipo_pessoa_case.label('tipo_pessoa'),
                                               ).join(InteressadoModel)


        res = res.group_by(InteressadoModel.Nome,
                  InteressadoModel.Cidade,
                  InteressadoModel.Uf,
                  InteressadoModel.Responsavel,
                  InteressadoModel.CgcCpf,
                  tipo_pessoa_case
        )

        
        res = res.filter(ProjetoModel.idProjeto.isnot(None))

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

        # order by descending
        if sort_order == 'desc':
            res = res.order_by(desc(sort_field))
        #order by ascending
        else:
            res = res.order_by(sort_field)

        total_records = res.count()

        res = res.slice(start_row, end_row)

        return res.all(), total_records
