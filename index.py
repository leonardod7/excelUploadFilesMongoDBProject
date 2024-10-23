# Importando as bibliotecas --------------------------------------------------------------------------------------------
from dash import html, Input, Output, State, dash, dcc, page_registry, _dash_renderer
import dash_mantine_components as dmc
from pages.listar_documento_button_2 import consultar_documentos_page
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

                 # Store na aplicação como um todo
                 # dcc.Store(id='id-data-cenarios-input-store', storage_type='session'),

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
    if pathname == '/inserir-documento':
        return html.H3("under construction")
    elif pathname == '/consultar-documentos':
        return consultar_documentos_page()
    elif pathname == '/home':
        return html.H3("Home")
    else:
        return consultar_documentos_page()  # Página padrão é o upload de documentos


# Rodando o app -------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=8058)
