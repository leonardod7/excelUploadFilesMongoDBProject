# Importando as bibliotecas --------------------------------------------------------------------------------------------
from dash import html, Input, Output, State, dash, dcc, page_registry, _dash_renderer

from pages.inserir_documento import upload_section_page

# Importando componentes do app ----------------------------------------------------------------------------------------
from app import *
from components.navbar import navbar

# Criando o app --------------------------------------------------------------------------------------------------------

app.layout = html.Div(className="index-div-app",
                      children=[

                          # Barra de navegação
                          navbar(),

                          # Store na aplicação como um todo
                          dcc.Store(id='', data="", storage_type='session'),

                          # Container de páginas
                          dcc.Location(id='url', refresh=False),

                          # Conteúdo do app
                          html.Div(className="index-div-content", id="page-content", children=[]),

                      ])


# Atualiza o conteúdo da página com base na URL
@app.callback(
    Output(component_id='page-content', component_property='children'),
    Input(component_id='url', component_property='pathname')
)
def display_page(pathname):
    if pathname == '/inserir-documento':
        return upload_section_page()
    elif pathname == '/consultar-documentos':
        return html.H3("Consultar Documentos")
    elif pathname == '/home':
        return html.H3("Home")
    else:
        return upload_section_page()  # Página padrão é o upload de documentos


if __name__ == '__main__':
    app.run(debug=True, port=8058)
