import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import uuid
import dash_bootstrap_components as dbc

# Inicializar o app
app = dash.Dash(__name__)

# Dados iniciais dos cenários
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

# Função para renderizar um card
def render_card(cenario):
    return dbc.Card(
        dbc.CardBody([
            html.H4(f"Cenário {cenario['cenario'][-1]}", className="card-title"),
            html.P(f"Empresa: {cenario['empresa']}", className="card-text"),
            html.P(f"Descrição: {cenario['descricao']}", className="card-text"),
            html.P(f"Data: {cenario['data']}", className="card-text"),
            html.P(f"Tipo: {cenario['tipo']}", className="card-text"),
            html.P(f"Parte: {cenario['parte']}", className="card-text"),
            html.Button(
                "🗑️", id={"type": "delete-button", "index": cenario["id"]}, n_clicks=0, className="btn btn-outline-danger"
            )
        ]),
        style={"width": "18rem", "margin": "10px"}
    )

# Layout do app
app.layout = html.Div([
    html.H1("Cenários de Parques Solares"),
    html.Div(id="cards-container", children=[render_card(cenario) for cenario in cenarios], style={"display": "flex", "flex-wrap": "wrap"}),
    dcc.Store(id="cenarios-store", data=cenarios)  # Armazenar os cenários
])

# Callback para excluir um card ao clicar no botão da lixeira
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
        # Remover o card do cenário pelo id
        cenarios = [cenario for cenario in cenarios if cenario["id"] != card_id_to_delete]
        return cenarios

# Callback para atualizar a interface com os cards restantes
@app.callback(
    Output("cards-container", "children"),
    Input("cenarios-store", "data")
)
def update_cards(cenarios):
    # Renderizar os cards atualizados
    return [render_card(cenario) for cenario in cenarios]

# Executar o app
if __name__ == "__main__":
    app.run_server(debug=True, port=8043)
