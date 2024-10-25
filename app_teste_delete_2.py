import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from bson import ObjectId  # Simulando o ObjectId do MongoDB

# Inicializando a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Função para converter ObjectId em string
def stringify_object_ids(data):
    for cenario, docs in data.items():
        for doc in docs:
            if '_id' in doc and isinstance(doc['_id'], ObjectId):
                doc['_id'] = str(doc['_id'])
    return data

# Dados em formatos não serealizados
data_final = {'Cenários': {'Cenário 2': [{'_id': ObjectId('67111516808999e3b2900018'), 'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:45:57.889000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 1}, {'_id': ObjectId('67111516808999e3b2900019'), 'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:45:57.928000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 2}, {'_id': ObjectId('67111516808999e3b290001a'), 'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:45:57.967000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 3}, {'_id': ObjectId('67111516808999e3b290001b'), 'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:45:58.011000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 4}], 'Cenário 1': [{'_id': ObjectId('6711153207ea80384ddb82e5'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:46:25.804000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 1}, {'_id': ObjectId('6711153207ea80384ddb82e6'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:46:25.847000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 2}, {'_id': ObjectId('6711153207ea80384ddb82e7'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:46:25.889000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 3}, {'_id': ObjectId('6711153207ea80384ddb82e8'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:46:25.936000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 4}, {'_id': ObjectId('6711158485d1d4c8dfd8fce3'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:47:48.514000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'bp', 'parte': 1}, {'_id': ObjectId('6711158485d1d4c8dfd8fce4'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:47:48.563000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'bp', 'parte': 2}, {'_id': ObjectId('6711158585d1d4c8dfd8fce5'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:47:48.612000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'bp', 'parte': 3}, {'_id': ObjectId('6711158585d1d4c8dfd8fce6'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:47:48.667000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'bp', 'parte': 4}]}}

# Convertendo ObjectIds para strings
data_final['Cenários'] = stringify_object_ids(data_final['Cenários'])

# Função para renderizar as divs dos cenários
def render_cenarios(cenarios_dict):
    cenarios_divs = []
    for cenario_nome, cenario_docs in cenarios_dict.items():
        print("Cenário Nome: --------")
        print(cenario_nome)
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
    html.Div(id="cenarios-div", children=render_cenarios(data_final['Cenários'])),
    dcc.Store(id='cenarios-store', data=data_final['Cenários'])
])

# Callback para deletar o cenário correspondente
@app.callback(
    [Output('cenarios-div', 'children'),
     Output('cenarios-store', 'data')],
    Input({'type': 'delete-btn', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State('cenarios-store', 'data')
)
def deletar_cenario(n_clicks, data):
    ctx = dash.callback_context
    print("Triggered context:", ctx.triggered)  # Adicionado para depuração

    # Verifica se nenhum botão foi clicado
    if not ctx.triggered or not n_clicks or all(click is None for click in n_clicks):
        return render_cenarios(data), data

    # Identifica o botão clicado
    btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print("Button ID:", btn_id)  # {"index":"Cenário 1","type":"delete-btn"}
    # Converte a string de volta ao dicionário
    btn_id = eval(btn_id)
    print("Button ID:", btn_id)  # Button ID: {'index': 'Cenário 1', 'type': 'delete-btn'}

    # Remove o cenário correspondente ao botão clicado
    cenario_nome = btn_id['index']
    if cenario_nome in data:
        del data[cenario_nome]

    # Retorna o layout atualizado e o novo estado do dcc.Store
    return render_cenarios(data), data

# Rodando o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True, port=8032)