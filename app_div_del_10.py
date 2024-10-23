import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
import uuid

# Inicializando o app
app = dash.Dash(__name__)

# Cenários (dados fictícios) -------------------------------------------------------------------------------------------
cenarios = [
    {"id": str(uuid.uuid4()), "cenario": "Cenário 1", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:45:57.889000", "tipo": "dre", "parte": 1},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 1", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:45:57.928000", "tipo": "dre", "parte": 2},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 1", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:45:57.967000", "tipo": "dre", "parte": 3},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 1", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:45:58.011000", "tipo": "dre", "parte": 4},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 2", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:47:48.514000", "tipo": "bp", "parte": 1},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 2", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:47:48.563000", "tipo": "bp", "parte": 2},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 2", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:47:48.612000", "tipo": "bp", "parte": 3},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 2", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:47:48.667000", "tipo": "bp", "parte": 4}
]

# Função de agrupamento por chave --------------------------------------------------------------------------------------
def agrupar_por_chave(lista: list[dict], chave: str):
    grupos = {}
    for item in lista:
        key = item[chave]
        if key not in grupos:
            grupos[key] = []
        grupos[key].append(item)
    return grupos

# Função para renderizar cards -----------------------------------------------------------------------------------------
def render_card(cenario) -> dbc.Card:
    card: dbc.Card = dbc.Card(
        dbc.CardBody([
            html.H4(children=[f"{cenario['cenario']}"], className="card-title", style={'fontFamily': 'Arial Narrow',
                                                                                       'fontSize': '14px',
                                                                                       'borderBottom': '2px solid gray',
                                                                                       'paddingBottom': '5px',
                                                                                       'marginTop': '5px',
                                                                                       'border-radius': '5px'}),

            html.P(children=[html.Span(children=["Parte: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                             f"{cenario['parte']}"], className="card-text", style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

            html.P(children=[html.Span(children=["Empresa: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                             f"{cenario['empresa']}"], className="card-text", style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

            html.P(children=[html.Span(children=["Descrição: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                             f"{cenario['descricao']}"], className="card-text", style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

            html.P(children=[html.Span(children=["Data: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                             f"{cenario['data']}"], className="card-text", style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

            html.P(children=[html.Span(children=["Tipo: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                             f"{cenario['tipo']}"], className="card-text", style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

            # Botão de exclusão
            dbc.Button(children=["🗑️"], id={"type": "delete-button", "index": cenario["id"]}, n_clicks=0, color="danger")
        ]),
        style={'border': '1px solid #ccc',
               'margin': '10px',
               'padding': '10px',
               'width': '300px',
               'background': "linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), "
                             "url('/assets/img/eolicas.jpg')",
               'backgroundSize': 'cover',
               'backgroundPosition': 'center',
               'border-radius': '10px'
               }
    )
    return card


# Layout principal do app ----------------------------------------------------------------------------------------------
app.layout = html.Div(children=[
    html.H3(children=["Cenários Salvos de Parques Solares"], style={"textAlign": "center", "color": "gray"}),
    html.Hr(),
    html.Div(id="cards-container"),  # Contêiner para os cards
    dcc.Store(id="cenarios-store", data=cenarios)  # Armazenando os cenários
], style={"padding": "20px"})


# 1) Callback para atualizar os cards com base nos dados ---------------------------------------------------------------

# 1.1) Callback para atualizar os cards com base nos dados -------------------------------------------------------------
@app.callback(
    Output(component_id="cards-container", component_property="children"),
    Input(component_id="cenarios-store", component_property="data")
)
def update_cards(cenarios: list[dict]):

    agrupado = agrupar_por_chave(lista=cenarios, chave="cenario")
    cards = []
    for grupo, itens in agrupado.items():
        div: html.Div = html.Div(children=[
            html.H3(children=[grupo], style={"textAlign": "center", "color": "gray"}),
            html.Div([render_card(item) for item in itens],  style={'display': 'flex',
                                                                    'flexDirection': 'space-around',
                                                                    'border': '1px solid gold',
                                                                    'padding': '10px'})
        ])
        # print(grupo)  # debug Cenário 1, Cenário 2, etc
        # print(itens)  # debug Lista com os dicionários dos cenários parte 1, 2, 3, 4.
        cards.append(div)  # Título do grupo

    return cards

# 1.2) Callback para excluir um card -----------------------------------------------------------------------------------
@app.callback(
    Output(component_id="cenarios-store", component_property="data"),
    Input(component_id={"type": "delete-button", "index": ALL}, component_property="n_clicks"),
    State(component_id="cenarios-store", component_property="data"),
    prevent_initial_call=True
)
def delete_card(n_clicks, cenarios):
    # Verificar se algum botão foi clicado
    if not any(n_clicks):
        return dash.no_update

    # Identificar o índice do botão clicado
    clicked_index = [i for i, click in enumerate(n_clicks) if click > 0][0]

    # Obter o ID do cenário a ser deletado
    card_id_to_delete = cenarios[clicked_index]["id"]

    # Remover o card com o ID correspondente
    cenarios = [cenario for cenario in cenarios if cenario["id"] != card_id_to_delete]

    return cenarios


# Executar o app
if __name__ == "__main__":
    app.run_server(debug=True, port=8023)


# callbacks originais --------------------------------------------------------------------------------------------------

# # 1.1) Callback para atualizar os cards com base nos dados -----------------------------------------------------------
# @app.callback(
#     Output(component_id="cards-container", component_property="children"),
#     Input(component_id="cenarios-store", component_property="data")
# )
# def update_cards(cenarios):
#     agrupado = agrupar_por_chave(lista=cenarios, chave="cenario")
#     cards = []
#     for grupo, itens in agrupado.items():
#
#         print(grupo)  # debug Cenário 1, Cenário 2, etc
#         print(itens)  # debug Lista com os dicionários dos cenários parte 1, 2, 3, 4.
#
#         cards.append(html.H3(grupo))  # Título do grupo
#         for item in itens:  # para cada dicionário na lista de dicionarios
#             cards.append(render_card(item))
#     return cards


# 1.2) Callback para excluir um card -----------------------------------------------------------------------------------
# @app.callback(
#     Output(component_id="cenarios-store", component_property="data"),
#     Input(component_id={"type": "delete-button", "index": ALL}, component_property="n_clicks"),
#     State(component_id="cenarios-store", component_property="data"),
#     prevent_initial_call=True
# )
# def delete_card(n_clicks, cenarios):
#     # Identificar o botão que foi clicado
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return cenarios
#     else:
#         triggered_id = eval(ctx.triggered[0]["prop_id"].split(".")[0])
#         card_id_to_delete = triggered_id["index"]
#         # Remover o card com o ID correspondente
#         cenarios = [cenario for cenario in cenarios if cenario["id"] != card_id_to_delete]
#         return cenarios