# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

import sys
sys.path.append('../..')
from app import app
from sql_connector import SQL_connector
from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, distinct
from flask import Flask
import urllib

import datetime, json



class MSSql_connector(SQL_connector):

    def __init__(self):

        if app.config['SQL_DRIVER'] == 'pymssql':
          engine = create_engine(r"mssql+pymssql://{0}:{1}@{2}/{3}".format( 
                                          app.config['DATABASE_USER'],
                                          app.config['DATABASE_PASSWORD'],
                                          app.config['DATABASE_HOST'],
                                          app.config['DATABASE_NAME']))

        else:
          quoted = urllib.quote_plus('DRIVER={FreeTDS};Server=%s;Database=%s;UID=%s;PWD=%s;TDS_Version=8.0;CHARSET=UTF8;Port=1433;'
                                          %(app.config['DATABASE_HOST'],
                                            app.config['DATABASE_NAME'],
                                            app.config['DATABASE_USER'],
                                            app.config['DATABASE_PASSWORD']))

          engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted), connect_args={'convert_unicode': True})
          
        # create a Session
        Session = sessionmaker(bind=engine)
        self.session = Session()


# def test():
#     print 'Testing class...'
#     sys.path.append('..')
#     from models import *
#     session = MSSql_connector().session
#     #res  = session.query(ProjetoModel).order_by(ProjetoModel.IdPRONAC).slice(1,2)
#
#     try:
#         #res  = session.query(func.sac.Modelo.fnValorDaProposta(ProjetoModel.idProjeto)).order_by(ProjetoModel.IdPRONAC).slice(1,10)
#         res = session.query(
#                             InteressadoModel.Nome
#                             ).join(CaptacaoModel).filter(InteressadoModel.Uf=='go')
#         for r in res:
#             print r
#      #      print json.dumps(r.to_dict())
#
#     except Exception as e:
#         print 'Error occured : '+str(e)
#
#     #res  = session.query(ProjetoModel).filter(ProjetoModel.IdPRONAC == 1).all()
#     #res = session.query(func.count(distinct(ProjetoModel.NomeProjeto)))
#
#     #data_dict = row2dict(res)
#     #print data_dict
#     #print dir(res)
#
#
# if __name__ == '__main__':
#     test()
