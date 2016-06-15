from sqlalchemy import func

import sys
sys.path.append('../')

#from config import DEFAULT_SQL_CONNECTOR as sql_connector
from database.connectors.mssql_connector import MSSql_connector as SQL_connector


class ModelsBase(object):
    def __init__(self):
        self.sql_connector = SQL_connector()

    def count(self, q):
      count_q = q.statement.with_only_columns([func.count()]).order_by(None)
      count = q.session.execute(count_q).scalar()
      return count or 0
