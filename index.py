# Importando as bibliotecas --------------------------------------------------------------------------------------------
from dash import html, Input, Output, State, dash, dcc, page_registry, _dash_renderer
import dash_mantine_components as dmc

from pages.inserir_documentos import inserir_documentos_page
from pages.listar_documento import consultar_documentos_page
from pages.home import home_page

_dash_renderer._set_react_version("18.2.0")

# Importando componentes do app ----------------------------------------------------------------------------------------
from app import *
from components.navbar import navbar

# Criando o app --------------------------------------------------------------------------------------------------------

app.layout = dmc.MantineProvider(
    html.Div(className="index-div-app",
             children=[

                 # Barra de navegação
                 navbar(),

                 # Armazenando os cenários
                 dcc.Store(id="id-cenarios-store"),
                 # Armazenando os cenários com o nome da colecao e do banco
                 dcc.Store(id="id-collection-db_names-store"),

                 dcc.Store(id='id-store-infotabela-usuario', storage_type='session'),  # Armazenamento de sessão

                 # Container de páginas
                 dcc.Location(id='url', refresh=False),

                 # Conteúdo do app
                 html.Div(className="index-div-content", id="page-content", children=[]),

             ])
)


# Atualiza o conteúdo da página com base na URL
@app.callback(
    Output(component_id='page-content', component_property='children'),
    Input(component_id='url', component_property='pathname')
)
def display_page(pathname):
    if pathname is None:
        return html.H3("Erro: Caminho não definido.")
    elif pathname == '/inserir-documento':
        return inserir_documentos_page()
    elif pathname == '/consultar-documentos':
        return consultar_documentos_page()
    elif pathname == '/home':
        return home_page()
    else:
        return consultar_documentos_page()  # Página padrão é o upload de documentos


# Rodando o app -------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=8064)
