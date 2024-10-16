import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from pymongo import MongoClient
import base64

# Conectando ao MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['empresas']

# Inicializando o app com Bootstrap para um visual melhor
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Função para salvar o arquivo no MongoDB
def salvar_arquivo_mongodb(contents, filename, empresa):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_excel(decoded)
    data = df.to_dict(orient='records')
    collection = db[empresa]
    collection.insert_many(data)

# Função para renderizar os blocos visuais dos bancos de dados
def renderizar_bancos():
    bancos = []
    empresas = ['empresa_1', 'empresa_2', 'empresa_3', 'empresa_4']
    for empresa in empresas:
        bancos.append(
            dbc.Card(
                dbc.CardBody([
                    html.Img(src='/assets/img/database.png', style={'width': '50%'}),
                    html.H5(f"Banco de {empresa.replace('_', ' ').title()}"),
                    dcc.Upload(
                        id=f'upload-{empresa}',
                        children=html.Div(['Arraste e solte ou ', html.A('selecione um arquivo')]),
                        style={
                            'width': '100%', 'height': '60px', 'lineHeight': '60px',
                            'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                            'textAlign': 'center', 'margin': '10px'
                        },
                        multiple=False
                    ),
                    html.Div(id=f'output-{empresa}')
                ]),
                style={'width': '23%', 'display': 'inline-block', 'margin': '10px'}
            )
        )
    return bancos

# Layout do app
app.layout = dbc.Container([
    html.H1('Database Manager for Companies', style={'textAlign': 'center', 'marginTop': '20px'}),
    html.P('Arraste os arquivos Excel para os respectivos bancos de dados.', style={'textAlign': 'center'}),

    # Exibição dos bancos de dados das empresas
    dbc.Row(
        renderizar_bancos(),
        justify='center'
    ),

    # Botão para atualizar informações
    html.Div(
        dbc.Button("Atualizar Informações", id="update-button", color="primary", className="mr-2"),
        style={'textAlign': 'center', 'marginTop': '20px'}
    ),

    # Alerta de confirmação
    dbc.Alert(id='alert', color='success', is_open=False, dismissable=True)
])

# Callback para lidar com o upload de arquivos e salvar no MongoDB
@app.callback(
    Output('alert', 'is_open'),
    Output('alert', 'children'),
    Output('alert', 'color'),
    [Input(f'upload-{empresa}', 'contents') for empresa in ['empresa_1', 'empresa_2', 'empresa_3', 'empresa_4']],
    [State(f'upload-{empresa}', 'filename') for empresa in ['empresa_1', 'empresa_2', 'empresa_3', 'empresa_4']],
    prevent_initial_call=True
)
def processar_upload(contents1, contents2, contents3, contents4, filename1, filename2, filename3, filename4):
    alert_message = ""
    alert_color = "success"
    empresas = ['empresa_1', 'empresa_2', 'empresa_3', 'empresa_4']
    contents = [contents1, contents2, contents3, contents4]
    filenames = [filename1, filename2, filename3, filename4]

    for i, content in enumerate(contents):
        if content:
            salvar_arquivo_mongodb(content, filenames[i], empresas[i])
            alert_message += f'Dados da {empresas[i].replace("_", " ").title()} enviados com sucesso! '

    if alert_message:
        return True, alert_message, alert_color
    else:
        return False, "", alert_color

# Rodando o app
if __name__ == '__main__':
    app.run_server(debug=True)
