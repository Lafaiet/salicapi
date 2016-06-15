from sqlalchemy import case, func

from ..ModelsBase import ModelsBase
from ..SharedModels import PreProjetoModel, MecanismoModel



class PreProjetoModelObject(ModelsBase):

    def __init__(self):
        super (PreProjetoModelObject,self).__init__()


    def all(self, limit, offset, id = None, nome = None, data_inicio = None, data_termino = None, extra_fields = False):

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

          total_records = self.count(res)

          res = res.slice(start_row, end_row)

          return res.all(), total_records
