from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import pandas as pd


class Cola:
    def cola_identica(df: pd.DataFrame) -> pd.DataFrame:
        df = df[df.drop('part', axis=1).duplicated(keep=False)]

        df = df.copy()
        df['part'] = df['part'].astype(str)

        agregar = [i for i in df.columns if i not in ['part','sistema']]
        return df.groupby(agregar, dropna=False)['part'].agg(lambda x: ' - '.join((x))).reset_index()
    


    def apply_model(df: pd.DataFrame, eps=0.05) -> pd.DataFrame:
        # Preenchendo vazios pela média da linha
        imputer = SimpleImputer(strategy="mean")
        df_model = imputer.fit_transform(df.T).T
  
        # Aplicando a normalização
        norm = StandardScaler()
        df_model = norm.fit_transform(df_model)
        df_model = pd.DataFrame(df_model)
        
        # Aplicando o modelo DBSCAN
        # eps = 0.05
        model = DBSCAN(eps=eps, min_samples=2)
        model = model.fit(df_model)
        
        df['cluster'] = model.labels_
        return df