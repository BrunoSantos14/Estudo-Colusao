from utils import Cola
from utils import PreProcessamento
from utils import Data
import pandas as pd



class Estudo:
    def __init__(self, ano: int, id_modulo: list[int], analito: list[str]):

        data = Data()
        self.parceiros = data.get_parceiros()
        self.modulos = data.get_modulos()
        self.df = data.get_data(ano=ano, id_modulo=id_modulo, analito=analito)


    def run(self) -> pd.DataFrame|None:
        df = self.df.copy()
        df = PreProcessamento(df).get_data()
        
        if not df.empty:
            lista = []

            # Para cada módulo
            for modulo in df.id_modulo.unique():
                aux = df[df.id_modulo == modulo]

                # Para cada analito
                for analito in aux.analito.unique():
                    aux2 = aux[aux.analito == analito]
                    cola = Cola(aux2.set_index(['part','id_modulo','analito','sistema']))
                    df_cluster = cola.aplicar_modelo(eps = None)
                    lista.append(df_cluster)

            df_cluster = pd.concat(lista)
        else:
            return None

        # Merge parceiros
        df_cluster = df_cluster.merge(
            self.parceiros,
            on = 'part'
        )

        # Merge modulos
        df_cluster = df_cluster.merge(
            self.modulos,
            on = 'id_modulo'
        )

        return df_cluster
