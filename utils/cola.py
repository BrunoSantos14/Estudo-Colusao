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
        self.df = self.df.reset_index()
        self.df = self.df[self.df.drop('part', axis=1).duplicated(keep=False)]

        self.df = self.df.copy()
        self.df['part'] = self.df['part'].astype(str)

        agregar = [i for i in self.df.columns if i not in ['part','sistema']]
        return self.df.groupby(agregar, dropna=False)['part'].agg(lambda x: ' - '.join((x))).reset_index()
        

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


    def aplicar_modelo(self, eps: float = None) -> dict[float, pd.DataFrame]:
        
        # Preenchendo vazios pela média da linha
        imputer = SimpleImputer(strategy="mean")
        dados: np.ndarray = imputer.fit_transform(self.df.T).T
        
        # Aplicando a normalização
        norm = StandardScaler()
        dados = norm.fit_transform(dados)

        # Aplicando o modelo DBSCAN
        if eps is None:
            eps = self.__get_eps(dados)
        
        model = DBSCAN(eps=eps, min_samples=self.__min_samples, n_jobs=-1).fit(dados)

        self.df['cluster'] = model.labels_

        return dict(
            eps_used = eps,
            df = self.df.query('cluster != -1').sort_values('cluster')
        )
    