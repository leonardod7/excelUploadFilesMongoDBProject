import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from bson import ObjectId  # Simulando o ObjectId do MongoDB

# Inicializando a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Simulando a estrutura de dados enviada
cenarios = {
    'Cenários': {
        'Cenário 2': [
            {'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:45:57.889000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 1},
            { 'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:45:57.928000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 2}
        ],
        'Cenário 1': [
            {'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:46:25.804000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 1},
            { 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:46:25.847000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 2}
        ]
    }
}

# Função para renderizar as divs dos cenários
def render_cenarios(cenarios_dict):
    cenarios_divs = []
    for cenario_nome, cenario_docs in cenarios_dict.items():
        cenarios_divs.append(html.Div([
            html.H3(f"{cenario_nome}"),
            html.Pre(str(cenario_docs), style={'white-space': 'pre-wrap'}),
            dbc.Button("Deletar", id={'type': 'delete-btn', 'index': cenario_nome}, color="danger", className="mt-2"),
            html.Hr()
        ], id=f"div-{cenario_nome}"))
    return cenarios_divs

# Layout do app
app.layout = html.Div([
    html.H1("Cenários"),
    html.Div(id="cenarios-div", children=render_cenarios(cenarios['Cenários'])),
    dcc.Store(id='cenarios-store', data=cenarios['Cenários'])
])

# Callback para deletar o cenário correspondente
@app.callback(
    Output(component_id='cenarios-div', component_property='children'),
    Input(component_id={'type': 'delete-btn', 'index': dash.dependencies.ALL}, component_property='n_clicks'),
    State(component_id='cenarios-store', component_property='data')
)
def deletar_cenario(n_clicks, data):
    ctx = dash.callback_context
    if not ctx.triggered or not any(n_clicks):
        return render_cenarios(data)

    # Identifica qual botão foi clicado
    btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
    btn_id = eval(btn_id)  # Converte a string de volta ao dicionário

    # Deleta o cenário correspondente
    cenario_nome = btn_id['index']
    if cenario_nome in data:
        del data[cenario_nome]

    # Atualiza a lista de cenários
    return render_cenarios(data)

# Rodando o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True, port=8032)

