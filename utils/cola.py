from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np


class Cola:
    __min_samples = 2
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def cola_identica(self) -> pd.DataFrame:
        df = self.df.reset_index()
        df = df[df.drop('part', axis=1).duplicated(keep=False)]

        # df = df.copy()
        # df['part'] = df['part'].astype(str)

        # agregar = [i for i in df.columns if i not in ['part','sistema']]
        # df = df.groupby(agregar, dropna=False)['part'].agg(lambda x: ' - '.join((x))).reset_index()
        df['identico'] = 'Sim'
        return df
        

    def __get_eps(self, dados: np.ndarray) -> float:
        neighbors = NearestNeighbors(n_neighbors=self.__min_samples)
        neighbors_fit = neighbors.fit(dados)
        distances, _ = neighbors_fit.kneighbors(dados)

        distances = np.mean(distances[:,1:], axis=1)
        distances = np.sort(distances)
        distances = distances[np.where(distances <= 2)]
        slopes = np.diff(distances)
        value = slopes[np.where(slopes>=1/100)][0]

        index = np.argmax(slopes==value)

        eps = distances[index+1]
        return eps


    def aplicar_modelo(self, eps: float=None) -> pd.DataFrame:
        cola_identica = self.cola_identica()
        
        df = self.df.copy()

        # Preenchendo vazios pela média da linha
        imputer = SimpleImputer(strategy="mean")
        dados: np.ndarray = imputer.fit_transform(df.T).T
        
        # Aplicando a normalização
        norm = StandardScaler()
        dados = norm.fit_transform(dados)

        # Aplicando o modelo DBSCAN
        if eps is None:
            eps = self.__get_eps(dados)
        
        model = DBSCAN(eps=eps, min_samples=self.__min_samples, n_jobs=-1).fit(dados)

        df['cluster'] = model.labels_
        df['eps_calculado'] = eps
        df = df.query('cluster != -1').reset_index()

        # Merge com colas identicas
        df = df.merge(
            cola_identica[['part','id_modulo','analito','sistema','identico']],
            on=['part','id_modulo','analito','sistema'],
            how='left'
        )

        df['identico'] = df['identico'].fillna('Não')

        df = df.sort_values(['id_modulo','analito','cluster'])

        return df
