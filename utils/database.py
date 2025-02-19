from sqlalchemy import create_engine, text
import pandas as pd


class Banco:
    _dbns = None
    _engine = None
    __data = None
    __query = None
    __params = None
    def __init__(self, database, host='localhost', user='postgres', password='postgres'):
        self.__database = database
        self.__host = host
        self.__user = user
        self.__password= password
        self._dbns = f'postgresql+psycopg2://{self.__user}:{self.__password}@{self.__host}:5432/{self.__database}'
        self.__getEngine(self._dbns)


    @classmethod
    def __getEngine(cls, dbns: str):
        if (dbns != cls._dbns)|(cls._engine is None):
            cls._engine = create_engine(dbns)
            if not cls.conn_is_ok(cls):
                raise AttributeError('Conexão falha')


    def conn_is_ok(self):
        try:
            with self._engine.connect() as conn:
                conn.exec_driver_sql("SELECT 1")
            return True
        except:
            return False


    def get_table(self, query:str, **params) -> pd.DataFrame:
        if (self.__params != params) | (query != self.__query):
            self.__params = params
            self.__query = query
            self.__data = pd.read_sql(sql=text(query), con=self._engine, params=params)
        return self.__data
    

    def get_table_paginated(self, query:str, page_size=10, page=1, **params) -> pd.DataFrame:
        query = query+self.__create_pagination(page_size, page)
        return self.get_table(query, **params)
    

    def __create_pagination(self, page_size, page):
        offset = (page - 1) * page_size
        return f' LIMIT {page_size} OFFSET {offset}'
