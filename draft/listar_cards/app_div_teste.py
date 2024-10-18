import dash
from dash import html, dcc, Input, Output, State
import uuid

app = dash.Dash(__name__)

# Exemplo de dados iniciais para os cenários e SPEs
cenarios = [
    {"id": str(uuid.uuid4()), "cenario": "Cenário 2", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:45:57", "tipo": "dre", "parte": 1},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 2", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:45:58", "tipo": "dre", "parte": 2},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 1", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:46:25", "tipo": "dre", "parte": 1},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 1", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:46:25", "tipo": "dre", "parte": 2},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 1", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:46:25", "tipo": "dre", "parte": 3},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 1", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:47:48", "tipo": "bop", "parte": 4}
]

# Função para renderizar os cards
def render_card(cenario):
    return html.Div(
        className="card",
        children=[
            html.H4(cenario["cenario"], className="card-title"),
            html.P(f"Empresa: {cenario['empresa']}", className="card-text"),
            html.P(f"Descrição: {cenario['descricao']}", className="card-text"),
            html.P(f"Data: {cenario['data']}", className="card-text"),
            html.P(f"Tipo: {cenario['tipo']}", className="card-text"),
            html.P(f"Parte: {cenario['parte']}", className="card-text"),
            html.Button(
                "🗑️", id={"type": "delete-button", "index": cenario["id"]}, n_clicks=0
            )
        ],
        style={"width": "30%", "display": "inline-block", "margin": "10px", "border": "2px solid #CCCCCC", "padding": "10px", "border-radius": "5px"}
    )

# Layout do app
app.layout = html.Div([
    html.H1("Gestão de Cenários"),
    html.Div(id="cards-container", children=[render_card(cenario) for cenario in cenarios]),
    dcc.Store(id='stored-cenarios', data=cenarios)
])

# Callback para excluir card
@app.callback(
    Output("stored-cenarios", "data"),
    Input({"type": "delete-button", "index": dash.dependencies.ALL}, "n_clicks"),
    State("stored-cenarios", "data"),
    prevent_initial_call=True
)
def delete_card(n_clicks, cenarios):
    ctx = dash.callback_context

    if not ctx.triggered:
        return cenarios
    else:
        triggered_button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        index_to_remove = eval(triggered_button_id)["index"]
        updated_cenarios = [c for c in cenarios if c["id"] != index_to_remove]
        return updated_cenarios

# Callback para atualizar o layout com base nos cards restantes
@app.callback(
    Output("cards-container", "children"),
    Input("stored-cenarios", "data")
)
def update_cards(cenarios):
    return [render_card(cenario) for cenario in cenarios]

if __name__ == '__main__':
    app.run_server(debug=True, port=8909)
