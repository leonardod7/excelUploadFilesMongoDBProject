import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import uuid

# Inicializando o app
app = dash.Dash(__name__)

# Cenários (dados fictícios)
cenarios = [
    {"id": str(uuid.uuid4()), "cenario": "Cenário 2", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:45:57.889000", "tipo": "dre", "parte": 1},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 2", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:45:57.928000", "tipo": "dre", "parte": 2},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 2", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:45:57.967000", "tipo": "dre", "parte": 3},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 2", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:45:58.011000", "tipo": "dre", "parte": 4},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 1", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:47:48.514000", "tipo": "bp", "parte": 1},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 1", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:47:48.563000", "tipo": "bp", "parte": 2},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 1", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:47:48.612000", "tipo": "bp", "parte": 3},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 1", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:47:48.667000", "tipo": "bp", "parte": 4}
]

# Função de agrupamento por chave
def agrupar_por_chave(lista, chave):
    grupos = {}
    for item in lista:
        key = item[chave]
        if key not in grupos:
            grupos[key] = []
        grupos[key].append(item)
    return grupos

# Função para renderizar cards
def render_card(cenario):
    return dbc.Card(
        dbc.CardBody([
            html.H4(children=[f"{cenario['cenario']}, Parte {cenario['parte']}"], className="card-title"),
            html.P(children=[f"Empresa: {cenario['empresa']}"], className="card-text"),
            html.P(children=[f"Descrição: {cenario['descricao']}"], className="card-text"),
            html.P(children=[f"Data: {cenario['data']}"], className="card-text"),
            html.P(children=[f"Tipo: {cenario['tipo']}"], className="card-text"),
            dbc.Button(children=["🗑️"], id={"type": "delete-button", "index": cenario["id"]}, n_clicks=0, color="danger")
        ]),
        style={"width": "18rem", "margin": "10px"}
    )

# Layout principal do app
app.layout = html.Div([
    html.H1("Cenários de Parques Solares"),
    html.Div(id="cards-container"),  # Contêiner para os cards
    dcc.Store(id="cenarios-store", data=cenarios)  # Armazenando os cenários
])

# Callback para atualizar os cards com base nos dados
@app.callback(
    Output("cards-container", "children"),
    Input("cenarios-store", "data")
)
def update_cards(cenarios):
    agrupado = agrupar_por_chave(cenarios, "cenario")
    cards = []
    for grupo, itens in agrupado.items():
        cards.append(html.H3(grupo))  # Título do grupo
        for item in itens:
            cards.append(render_card(item))
    return cards

# Callback para excluir um card
@app.callback(
    Output("cenarios-store", "data"),
    Input({"type": "delete-button", "index": dash.dependencies.ALL}, "n_clicks"),
    State("cenarios-store", "data"),
    prevent_initial_call=True
)
def delete_card(n_clicks, cenarios):
    # Identificar o botão que foi clicado
    ctx = dash.callback_context
    if not ctx.triggered:
        return cenarios
    else:
        triggered_id = eval(ctx.triggered[0]["prop_id"].split(".")[0])
        card_id_to_delete = triggered_id["index"]
        # Remover o card com o ID correspondente
        cenarios = [cenario for cenario in cenarios if cenario["id"] != card_id_to_delete]
        return cenarios

# Executar o app
if __name__ == "__main__":
    app.run_server(debug=True)
