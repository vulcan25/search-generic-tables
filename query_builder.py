import sqlite3
from flask import g

DATABASE = 'tmp.sql'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

class CustomQuery():
    """
      Takes a query and parameters and you can get back headers, and rows.
    """
    def __init__(self, query, params = False):
        self.query = query

        # If params is not false, ensure it's a tuple:
        if params and type(params) is not tuple:
            raise Exception('params must be tuple')

        self.params = params
        
        self._run_query()

    def _run_query(self):
        with get_db() as sess:
          if self.params:
              c = sess.execute(self.query, self.params)
          else:
              c = sess.execute(self.query)

          self.rows = c.fetchall()
          self.headers = [i[0] for i in c.description]

    def result(self):
        return self.headers, self.rows