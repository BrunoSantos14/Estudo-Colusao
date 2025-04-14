from utils import Cola
from utils import PreProcessamento
from utils import Data
import pandas as pd



class Estudo:
    def __init__(self, ano: int, id_modulo: list[int]=None, analito: list[str]=None):

        data = Data()
        self.parceiros = data.get_parceiros()
        self.modulos = data.get_modulos()
        self.df = data.get_data(ano=ano, id_modulo=id_modulo, analito=analito)


    # def run(self):
    #     df = self.df.copy()
    #     df = PreProcessamento(df).get_data()
        
    #     if not df.empty:
    #         lista = []
    #         erros = []
    #         # Para cada módulo
    #         for modulo in df.id_modulo.unique():
    #             aux = df[df.id_modulo == modulo]

    #             # Para cada analito
    #             for analito in aux.analito.unique():
    #                 aux2 = aux[aux.analito == analito].dropna(how='all', axis=1)
    #                 cola = Cola(aux2.set_index(['part','id_modulo','analito','sistema']))
    #                 try:
    #                     df_cluster = cola.aplicar_modelo(eps = None)
    #                 except Exception as e:
    #                     erros.append((modulo, analito, e))
    #                     df_cluster = cola.aplicar_modelo(eps = 0.02)

    #                 lista.append(self.__merges(df_cluster))

    #     else:
    #         return None

    #     return lista, pd.DataFrame(erros, columns=['id_modulo','analito','erro'])

    def run(self):
        df = self.df.copy()
        df = PreProcessamento(df).get_data()
        
        if not df.empty:
            dic = {}
            erros = []
            # Para cada módulo
            for modulo in df.id_modulo.unique():
                dic[modulo] = []
                aux = df[df.id_modulo == modulo]

                # Para cada analito
                for analito in aux.analito.unique():
                    aux2 = aux[aux.analito == analito].dropna(how='all', axis=1)
                    cola = Cola(aux2.set_index(['part','id_modulo','analito','sistema']))
                    try:
                        df_cluster = cola.aplicar_modelo(eps = None)
                    except Exception as e:
                        erros.append((modulo, analito, e))
                        df_cluster = cola.aplicar_modelo(eps = 0.02)

                    dic[modulo].append(self.__merges(df_cluster))
            
            if len(erros) > 0:
                dic['erros'] = pd.DataFrame(erros, columns=['id_modulo','analito','erro'])

            return dic
        
        return None

    

    def __merges(self, df: pd.DataFrame) -> pd.DataFrame:
        # Merge parceiros
        df = df.merge(
            self.parceiros,
            on = 'part'
        )

        # Merge modulos
        df = df.merge(
            self.modulos,
            on = 'id_modulo'
        )

        return df
