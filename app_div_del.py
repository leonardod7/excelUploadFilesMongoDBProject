# TODO: Esse app simula a exclusão de divs de um layout do Dash. Cada div possui um botão de exclusão que, ao ser clicado, remove a div do layout.
# TODO: Ele não possui conexão com o banco de dados, mas simula a exclusão de documentos de uma coleção.

import dash
from dash import dcc, html, Input, Output, State
import datetime

# Lista de dicionários
lista_dict = [
    {'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime.datetime(2024, 10, 17, 10, 45, 57, 889000), 'empresa': 'Parque Solar 1', 'tipo': 'dre',
     'parte': 1},
    {'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime.datetime(2024, 10, 17, 10, 45, 57, 928000), 'empresa': 'Parque Solar 1', 'tipo': 'dre',
     'parte': 2},
    {'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime.datetime(2024, 10, 17, 10, 45, 57, 967000), 'empresa': 'Parque Solar 1', 'tipo': 'dre',
     'parte': 3},
    {'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime.datetime(2024, 10, 17, 10, 45, 57, 967000), 'empresa': 'Parque Solar 1', 'tipo': 'dre',
     'parte': 4},
]

# Criação do aplicativo Dash
app = dash.Dash(__name__)


conteudo: html.Div = html.Div(
    className="div-content",
    id='content',
    children=[
        # Div das informações
        html.Div(
            id=f'div-{i}',
            children=[
                html.H4(children=[d['nome']],
                        style={'fontFamily': 'Arial Narrow',
                               'fontSize': '14px',
                               'borderBottom': '2px solid gray',
                               'paddingBottom': '5px',
                               'marginTop': '5px',
                               'border-radius': '5px'}),

                html.P(children=[
                    html.Span(children=["Empresa: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                    f"{d['empresa']}"], style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

                html.P(children=[
                    html.Span(children=["Descrição: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                    f"{d['descricao']}"], style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

                html.P(children=[
                    html.Span(children=["Data: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                    f"{d['data']}"], style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

                html.P(children=[
                    html.Span(children=["Tipo: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                    f"{d['tipo']}"], style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

                html.P(children=[
                    html.Span(children=["Parte: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                    f"{d['parte']}"], style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

                html.Button(children=['🗑️'], id={'type': 'delete-button', 'index': i}, n_clicks=0)
            ],
            style={'border': '1px solid #ccc',
                   'margin': '10px',
                   'padding': '10px',
                   'width': '300px',
                   'background': "linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), "
                                 "url('/assets/img/eolicas.jpg')",  # Aplicando transparência na imagem
                   'backgroundSize': 'cover',  # Ajusta a imagem para cobrir a div
                   'backgroundPosition': 'center',  # Centraliza a imagem
                   'border-radius': '10px'
                   }
        ) for i, d in enumerate(lista_dict)
    ], style={'display': 'flex',
              'flexDirection': 'space-evenly',
              'border': '1px solid gold',
              'padding': '10px'}
)


# Layout do aplicativo ------------------------------------------------------------------------------------------------
app.layout = html.Div(children=[

    conteudo,
    html.Div(id='hidden-div', style={'display': 'none'})
], style={'margin': '20px',
          'border': '1px solid black',
          'display': 'flex',
          'alignItems': 'center',
          'justifyContent': 'center'}
)


# Callback para deletar divs
@app.callback(
    Output(component_id='content', component_property='children'),
    Output(component_id='hidden-div', component_property='children'),
    Input(component_id={'type': 'delete-button', 'index': dash.dependencies.ALL}, component_property='n_clicks'),
    State(component_id='content', component_property='children'),
    prevent_initial_call=True
)
def delete_div(n_clicks, children):
    # Filtra os índices que foram clicados
    indexes_to_delete = [i for i, clicks in enumerate(n_clicks) if clicks > 0]

    # Filtra as divs que não foram deletadas
    new_children = [child for i, child in enumerate(children) if i not in indexes_to_delete]

    return new_children, []


# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True, port=8976)
