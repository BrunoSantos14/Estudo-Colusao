from utils import Banco
from dotenv import load_dotenv
from typing import Literal
import os

load_dotenv()

class Data:
    __data = None
    __ano = None
    __id_modulo = None
    __analito = None

    banco = Banco(
        database=os.getenv('DATABASE'),
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD')
    )

    def get_parceiros(self):
        with open(f'querys/parceiros.sql', 'r') as file:
            query = file.read()
        return self.banco.get_table(query)
    

    def get_modulos(self):
        with open(f'querys/modulos.sql', 'r') as file:
            query = file.read()
        return self.banco.get_table(query)
    

    def get_data(self, ano: int, id_modulo: list|None=None, analito: list|None=None):
        if self.__data is None or self.__ano != ano or self.__id_modulo != id_modulo or self.__analito != analito:
            with open(f'querys/dados.sql', 'r') as file:
                query = file.read()
                self.__ano = ano
                self.__id_modulo = id_modulo
                self.__analito = analito
                self.__data = self.banco.get_table(query, ano=ano, id_modulo=id_modulo, analito=analito)
        
        return self.__data
        