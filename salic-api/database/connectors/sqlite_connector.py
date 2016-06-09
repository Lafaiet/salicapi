from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, distinct
from PreProjetoORM import *

import datetime


# create a Session
Session = sessionmaker(bind=engine)
session = Session()

res = session.query(func.count(distinct(PreProjetoModel.NomeProjeto)))

for r in res:
    print r