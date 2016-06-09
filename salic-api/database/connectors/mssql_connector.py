# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

import sys
sys.path.append('../..')
from config import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME
from sql_connector import SQL_connector
from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, distinct
from flask import Flask

import datetime, json
        


class MSSql_connector(SQL_connector):

    def __init__(self):
        engine = create_engine('mssql+pymssql://%s:%s@%s/%s?charset=utf8'
                                    %(DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME))

        # create a Session
        Session = sessionmaker(bind=engine)
        self.session = Session()
                        
    
def test():
    print 'Testing class...'
    sys.path.append('..')
    from models import *
    session = MSSql_connector().session
    #res  = session.query(ProjetoModel).order_by(ProjetoModel.IdPRONAC).slice(1,2)
    
    try:
        #res  = session.query(func.sac.Modelo.fnValorDaProposta(ProjetoModel.idProjeto)).order_by(ProjetoModel.IdPRONAC).slice(1,10)
        res = session.query(
                            InteressadoModel.Nome
                            ).join(CaptacaoModel).filter(InteressadoModel.Uf=='go')
        for r in res:
            print r
     #      print json.dumps(r.to_dict())
     
    except Exception as e:
        print 'Error occured : '+str(e)
    
    #res  = session.query(ProjetoModel).filter(ProjetoModel.IdPRONAC == 1).all()
    #res = session.query(func.count(distinct(ProjetoModel.NomeProjeto)))
                             
    #data_dict = row2dict(res)
    #print data_dict
    #print dir(res)
    
       
if __name__ == '__main__':
    test()