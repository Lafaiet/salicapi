from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, Integer, String, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import column_property



Base = declarative_base()

class ProjetoModel(Base):

    __tablename__ = 'Projetos'
    IdPRONAC = Column(Integer, primary_key=True)
    AnoProjeto = Column(String)
    Sequencial = Column(String)
    PRONAC = column_property(AnoProjeto + Sequencial)
    NomeProjeto = Column(String)
    DtInicioExecucao = Column(Date)
    DtFimExecucao = Column(Date)

    UfProjeto = Column(String)

    SolicitadoReal  = Column(String)
    SolicitadoUfir  = Column(String)
    SolicitadoCusteioUfir  = Column(String)
    SolicitadoCusteioReal  = Column(String)
    SolicitadoCapitalUfir = Column(String)
    SolicitadoCapitalReal = Column(String)

    ResumoProjeto = Column(Text)
    ProvidenciaTomada = Column(String)

    Segmento = Column(String, ForeignKey("Segmento.Codigo"))
    Segmento_related = relationship("SegmentoModel", foreign_keys=[Segmento])

    Situacao = Column(String, ForeignKey("Situacao.Codigo"))
    Situacao_related = relationship("SituacaoModel", foreign_keys=[Situacao])

    Area = Column(String, ForeignKey("Area.Codigo"))
    Area_related = relationship("AreaModel", foreign_keys=[Area])

    CgcCpf = Column(String, ForeignKey("Interessado.CgcCpf"))
    Interessado_related = relationship("InteressadoModel", foreign_keys=[CgcCpf])

    idProjeto = Column(Integer, ForeignKey("PreProjeto.idPreProjeto"))
    preprojeto_related = relationship("PreProjetoModel", foreign_keys=[idProjeto])

    Mecanismo = Column(String, ForeignKey("Mecanismo.Codigo"))
    mecanismo_related = relationship("MecanismoModel", foreign_keys=[Mecanismo])

    def __init__(self):
        pass


class PreProjetoModel(Base):

    __tablename__ = 'PreProjeto'
    idPreProjeto = Column(Integer, primary_key=True)
    NomeProjeto = Column(String)
    DtInicioDeExecucao = Column(Date)
    DtFinalDeExecucao = Column(Date)
    dtAceite = Column(Date)
    DtArquivamento = Column(Date)

    Mecanismo = Column(String, ForeignKey("Mecanismo.Codigo"))
    mecanismo_related = relationship("MecanismoModel", foreign_keys=[Mecanismo])

    Objetivos = Column(String)
    Justificativa  = Column(String)
    Acessibilidade  = Column(String)
    DemocratizacaoDeAcesso  = Column(String)
    EtapaDeTrabalho  = Column(String)
    FichaTecnica  = Column(String)
    ResumoDoProjeto = Column(String)
    Sinopse = Column(String)
    ImpactoAmbiental = Column(String)
    EspecificacaoTecnica = Column(String)
    EstrategiadeExecucao = Column(String)


    def __init__(self):
        pass

class SegmentoModel(Base):

    __tablename__ = 'Segmento'
    Codigo = Column(String, primary_key=True)
    Descricao = Column(String)

    def __init__(self):
        pass

class EnquadramentoModel(Base):

    __tablename__ = 'Enquadramento'
    IdEnquadramento = Column(Integer, primary_key=True)
    Enquadramento = Column(Integer)
    AnoProjeto = Column(String)
    Sequencial = Column(String)
    IdPRONAC = Column(Integer, ForeignKey('ProjetoModel.IdPRONAC'))

    def __init__(self):
        pass

class MecanismoModel(Base):

    __tablename__ = 'Mecanismo'
    Codigo = Column(Integer, primary_key=True)
    Descricao = Column(String)

    def __init__(self):
        pass

class SituacaoModel(Base):

    __tablename__ = 'Situacao'
    Codigo = Column(String, primary_key=True)
    Descricao = Column(String)

    def __init__(self):
        pass

class AreaModel(Base):

    __tablename__ = 'Area'
    Codigo = Column(String, primary_key=True)
    Descricao = Column(String)

    def __init__(self):
        pass

class InteressadoModel(Base):

    __tablename__ = 'Interessado'
    CgcCpf = Column(String, primary_key=True)
    Nome = Column(String)
    Responsavel = Column(String)
    Uf = Column(String)
    Cidade = Column(String)
    tipoPessoa = Column(String)

    captacao_related = relationship('CaptacaoModel', primaryjoin='InteressadoModel.CgcCpf==CaptacaoModel.CgcCpfMecena')
    projeto_related = relationship('ProjetoModel', primaryjoin='InteressadoModel.CgcCpf==ProjetoModel.CgcCpf')

    def __init__(self):
        pass

class CaptacaoModel(Base):

    __tablename__ = 'Captacao'
    Idcaptacao = Column(Integer, primary_key=True)
    AnoProjeto = Column(String)
    Sequencial = Column(String)
    PRONAC = column_property    (AnoProjeto + Sequencial)
    CaptacaoReal = Column(String)
    DtRecibo = Column(Date)

    CgcCpfMecena = Column(String, ForeignKey('Interessado.CgcCpf'))
    interessado_related = relationship('InteressadoModel', foreign_keys=[CgcCpfMecena])

    projeto_related = relationship('ProjetoModel', primaryjoin='CaptacaoModel.PRONAC==ProjetoModel.PRONAC')
