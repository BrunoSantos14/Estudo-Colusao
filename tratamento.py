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
    def __criar_col_item(cls, df: pd.DataFrame) -> pd.DataFrame:
        df['envio'] = pd.to_datetime(df['envio'])
        df['ano'] = df.envio.dt.year - 2000
        df['mes'] = df.envio.dt.month

        # Criando a coluna rodada
        df.loc[df.mes.isin([10, 11, 12]), 'rodada'] = '1'
        df.loc[df.mes.isin([1, 2, 3]), 'rodada'] = '2'
        df.loc[df.mes.isin([4, 5, 6]), 'rodada'] = '3'
        df.loc[df.mes.isin([7, 8, 9]), 'rodada'] = '4'

        # Deixando a coluna ano apenas com dois dígitos
        df.loc[df.rodada == '1', 'ano'] += 1  # Colocando itens da primeira rodada para o próximo ano
        df.ano = df.ano.astype(str)

        # Criando a coluna item
        df['num_item'] = df.item_ensaio.apply(lambda x: x[-1])
        df['item'] = 'A' + df.ano +  \
                    'R' + df.rodada +  \
                    'I' + df.num_item

        return df.drop(columns=['ano', 'mes', 'rodada', 'num_item'], axis=1)


    @classmethod
    def __pivotar(cls, df: pd.DataFrame) -> pd.DataFrame:
        qtd_itens_rodada = df.groupby(['id_modulo', 'analito', 'envio'])['item_ensaio'].transform(lambda x: len(set(x)))
        qtd_rodadas = df.groupby(['id_modulo', 'analito'])['envio'].transform(lambda x: len(set(x)))
        df['qtd_itens_validos'] = qtd_itens_rodada * qtd_rodadas
        
        return df.pivot_table(
                    values='valor',
                    index=['part', 'id_modulo' ,'analito', 'sistema', 'qtd_itens_validos'],
                    columns='item'
                ).reset_index()


    @classmethod
    def __filtrar_60_resp(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Filtrar participantes com mínimo 60% de respostas por item."""
        pattern = re.compile('A\d+R\d+I\d+')
        colunas_item = [re.match(pattern, coluna).group() for coluna in df.columns if re.match(pattern, coluna)]
        perc_respondido = df[colunas_item].count(axis=1) / df['qtd_itens_validos']
        return df.loc[perc_respondido >= 0.6].drop('qtd_itens_validos', axis=1)
    

    @classmethod
    def __tratamento(cls, df: pd.DataFrame) -> pd.DataFrame:
        df = cls.__criar_col_item(df)
        df = cls.__pivotar(df)
        return cls.__filtrar_60_resp(df)
    