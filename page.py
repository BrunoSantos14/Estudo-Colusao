import streamlit as st
from utils import Data
from estudo import Estudo
import re

class Page():
    def __init__(self):
        self.data = Data()
        
        # Inicialização do session_state
        if 'id_modulo' not in st.session_state:
            st.session_state.id_modulo = []
        
        if 'ano' not in st.session_state:
            st.session_state.ano = 2024
        
        if 'botao_clicado' not in st.session_state:
            st.session_state.botao_clicado = False

    def settings(self):
        st.set_page_config(
            page_title='Controllab',
            page_icon='https://controllab.com/wp-content/uploads/favicon-32x32-1.png',
            layout='wide'
        )
        st.image(
            'https://controllab.com/wp-content/uploads/logo_controllab_secundario_COR.png',
            width=200
        )
        st.title('Estudo de Colusão')

    def get_variaveis(self):
        # Criar lista de opções formatadas
        df_modulos = self.data.get_modulos()
        opcoes_modulo = [
            (row['id_modulo'], f"{row['modulo']} - {row['segmento']}") 
            for _, row in df_modulos.iterrows()
        ]
        
        # Widget único
        opcoes_selecionadas = st.sidebar.multiselect(
            'Módulo - Proficiência',
            options=[op[1] for op in opcoes_modulo],
            default=[
                op[1] for op in opcoes_modulo 
                if op[0] in st.session_state.id_modulo
            ],
            key='modulo_proficiencia_select'
        )
        
        # Mapeia seleções para id_modulo
        st.session_state.id_modulo = [
            op[0] for op in opcoes_modulo 
            if op[1] in opcoes_selecionadas
        ]

    def sidebar(self):
        st.sidebar.title('Configurações')
        st.session_state.ano = st.sidebar.selectbox(
            'Ano',
            [2024, 2023, 2022],
            index=[2024, 2023, 2022].index(st.session_state.ano),
            key='ano_select'
        )
        self.get_variaveis()
        
        if st.sidebar.button('Confirmar'):
            st.session_state.botao_clicado = True

    def estudo(self):
        if st.session_state.botao_clicado:
            modulo = [int(i) for i in st.session_state.id_modulo] if st.session_state.id_modulo else None

            with st.spinner("Carregando...", show_time=True):
                dic, erros = Estudo(
                    ano=st.session_state.ano,
                    id_modulo=modulo,
                    analito=None,
                ).run()

            modulos = []
            for id_mod in dic:
                lista = dic.get(id_mod)
                modulo_nome = lista[0].modulo.unique()[0]
                proficiencia_nome = lista[0].segmento.unique()[0]
                modulos.append((id_mod, modulo_nome, proficiencia_nome))

            abas = st.tabs([i[1] for i in modulos])
            for i, aba in enumerate(abas):
                with aba:
                    proficiencia = modulos[i][2]
                    st.markdown(f'### <center><u><b>{proficiencia}', True)

                    id_mod = modulos[i][0]
                    dfs = dic.get(id_mod)
                    for df in dfs:
                        analito = df.analito.unique()[0]
                        st.markdown(f'### {analito}:')

                        encontrar_col_item = lambda x: x if re.compile(r'A[0-9]+M[0-9]+I[0-9]+').findall(x) != [] else None
                        colunas_item = list(filter(encontrar_col_item, df.columns))
                        
                        colunas = ['part','grupo','regiao','sistema','eps_calculado','cluster','identico']+colunas_item
                        st.dataframe(df[colunas], hide_index=True)

    def main(self):
        self.settings()
        self.sidebar()
        self.estudo()

if __name__ == '__main__':
    page = Page()
    page.main()