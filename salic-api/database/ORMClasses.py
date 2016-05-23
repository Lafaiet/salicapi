from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, Integer, String, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import column_property



Base = declarative_base()

class ProjetoDb(Base):
    
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
    Segmento_related = relationship("SegmentoDb", foreign_keys=[Segmento])
    
    Situacao = Column(String, ForeignKey("Situacao.Codigo"))
    Situacao_related = relationship("SituacaoDb", foreign_keys=[Situacao])
    
    Area = Column(String, ForeignKey("Area.Codigo"))
    Area_related = relationship("AreaDb", foreign_keys=[Area])
    
    CgcCpf = Column(String, ForeignKey("Interessado.CgcCpf"))
    Interessado_related = relationship("InteressadoDb", foreign_keys=[CgcCpf])
    
    idProjeto = Column(Integer, ForeignKey("PreProjeto.idPreProjeto"))
    preprojeto_related = relationship("PreProjetoDb", foreign_keys=[idProjeto])
    
    Mecanismo = Column(String, ForeignKey("Mecanismo.Codigo"))
    mecanismo_related = relationship("MecanismoDb", foreign_keys=[Mecanismo])
        
    def __init__(self):
        pass


class PreProjetoDb(Base):
    
    __tablename__ = 'PreProjeto'
    idPreProjeto = Column(Integer, primary_key=True)
    NomeProjeto = Column(String)
    DtInicioDeExecucao = Column(Date)
    DtFinalDeExecucao = Column(Date)
    dtAceite = Column(Date)
    DtArquivamento = Column(Date)
    
    Mecanismo = Column(String, ForeignKey("Mecanismo.Codigo"))
    mecanismo_related = relationship("MecanismoDb", foreign_keys=[Mecanismo])

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
    
class SegmentoDb(Base):
    
    __tablename__ = 'Segmento'
    Codigo = Column(String, primary_key=True)
    Descricao = Column(String)
    
    def __init__(self):
        pass

class EnquadramentoDb(Base):
    
    __tablename__ = 'Enquadramento'
    IdEnquadramento = Column(Integer, primary_key=True)
    Enquadramento = Column(Integer)
    AnoProjeto = Column(String)
    Sequencial = Column(String)
    IdPRONAC = Column(Integer, ForeignKey('ProjetoDb.IdPRONAC'))
    
    def __init__(self):
        pass

class MecanismoDb(Base):
    
    __tablename__ = 'Mecanismo'
    Codigo = Column(Integer, primary_key=True)
    Descricao = Column(String)
    
    def __init__(self):
        pass      

class SituacaoDb(Base):
    
    __tablename__ = 'Situacao'
    Codigo = Column(String, primary_key=True)
    Descricao = Column(String)
    
    def __init__(self):
        pass

class AreaDb(Base):
    
    __tablename__ = 'Area'
    Codigo = Column(String, primary_key=True)
    Descricao = Column(String)
    
    def __init__(self):
        pass

class InteressadoDb(Base):
    
    __tablename__ = 'Interessado'
    CgcCpf = Column(String, primary_key=True)
    Nome = Column(String)
    Responsavel = Column(String)
    Uf = Column(String)
    Cidade = Column(String)
    tipoPessoa = Column(String)
    
    captacao_related = relationship('CaptacaoDb', primaryjoin='InteressadoDb.CgcCpf==CaptacaoDb.CgcCpfMecena')
    projeto_related = relationship('ProjetoDb', primaryjoin='InteressadoDb.CgcCpf==ProjetoDb.CgcCpf')
    
    def __init__(self):
        pass
    
class CaptacaoDb(Base):
    
    __tablename__ = 'Captacao'
    Idcaptacao = Column(Integer, primary_key=True)
    AnoProjeto = Column(String)
    Sequencial = Column(String)
    PRONAC = column_property    (AnoProjeto + Sequencial)
    CaptacaoReal = Column(String)
    DtRecibo = Column(Date)
    
    CgcCpfMecena = Column(String, ForeignKey('Interessado.CgcCpf'))
    interessado_related = relationship('InteressadoDb', foreign_keys=[CgcCpfMecena])

    projeto_related = relationship('ProjetoDb', primaryjoin='CaptacaoDb.PRONAC==ProjetoDb.PRONAC')

        