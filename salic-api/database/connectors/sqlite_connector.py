from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, distinct
from PreProjetoORM import *

import datetime
        
    
engine = create_engine('sqlite:///sqlalchemy_example.db')


# create a Session
Session = sessionmaker(bind=engine)
session = Session()

res = session.query(func.count(distinct(PreProjetoDb.NomeProjeto)))

for r in res:
    print r