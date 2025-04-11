import pandas as pd
import re


class PreProcessamento:
    _df: pd.DataFrame = None
    _df_tratado: pd.DataFrame = None

    def __init__(self, df: pd.DataFrame):
        self._df = df
        self.__getDF(self._df)


    def get_data(self) -> pd.DataFrame:
        return self._df_tratado


    @classmethod
    def __getDF(cls, df: pd.DataFrame):
        if (not df.equals(cls._df))|(cls._df is None):
            cls._df = df
            cls._df_tratado = cls.__tratamento(df)    
        

    @classmethod
    def __excluir_full_zero(cls, df: pd.DataFrame):
        """Excluir participantes com todos os reportes sendo 0."""
        parts_excluir = df.groupby(['id_modulo','analito','part'], as_index=False).valor.agg('sum').query('valor==0').part.values
        return df.loc[~df.part.isin(parts_excluir)]


    @classmethod
    def __criar_col_item(cls, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy(deep=True) # evitando warning
        df['envio'] = pd.to_datetime(df['envio'])
        df['ano'] = df.envio.dt.year - 2000
        df['mes'] = df.envio.dt.month

        # Deixando a coluna ano apenas com dois dígitos
        df.loc[df.mes.isin([10,11,12]), 'ano'] += 1  # Colocando itens da primeira rodada para o próximo ano

        # Criando a coluna item
        # df['num_item'] = df.item_ensaio.apply(lambda x: x[-1])
        df['num_item'] = df.item_ensaio.map(lambda x: re.compile('\w([0-9]+)').findall(x)[-1])

        df['item'] = 'A' + df.ano.astype(str) + \
                     'M' + df.mes.astype(str) + \
                     'I' + df.num_item

        return df.drop(columns=['ano', 'mes', 'num_item'], axis=1)


    @classmethod
    def __pivotar(cls, df: pd.DataFrame) -> pd.DataFrame:        
        return df.pivot_table(
                    values='valor',
                    index=['part', 'id_modulo' ,'analito', 'sistema'],
                    columns='item'
                ).reset_index()


    @classmethod
    def __filtrar_60_resp(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Filtrar participantes com mínimo 60% de respostas por item."""
        df['qtd_total_itens'] = df.groupby(['id_modulo','analito']).item.transform(lambda x: len(set(x)))
        df['qtd_itens_part'] = df.groupby(['id_modulo','analito','part','sistema']).item.transform(lambda x: len(set(x)))

        df = df.loc[df.qtd_itens_part >= df.qtd_total_itens * 0.6]
        df = df.drop(['qtd_total_itens','qtd_itens_part'], axis=1)
        return df
    

    @classmethod
    def __tratamento(cls, df: pd.DataFrame) -> pd.DataFrame:
        df = cls.__excluir_full_zero(df)
        df = cls.__criar_col_item(df)
        df = cls.__filtrar_60_resp(df)
        df = cls.__pivotar(df)
        
        # Excluir analitos com apenas 1 participante
        df = df.groupby(['id_modulo','analito']).filter(lambda grupo: len(grupo) > 1)
        return df
    