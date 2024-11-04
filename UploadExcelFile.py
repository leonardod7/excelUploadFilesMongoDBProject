import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import base64
import io

# Inicializa o app Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    html.H2("Upload de Arquivo Excel"),

    # Componente de upload
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Arraste e solte ou ',
            html.A('selecione um arquivo')
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px auto'
        },
        # Permite múltiplos arquivos
        multiple=False
    ),

    # Tabela para exibir as 10 primeiras linhas
    html.Div(id='output-table')
])

# Função para ler o arquivo Excel e gerar uma tabela Dash
def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        # Lê o arquivo Excel
        df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        return html.Div([
            'Erro ao processar o arquivo: {}'.format(e)
        ])

    # Seleciona as 10 primeiras linhas
    df = df.head(10)

    # Converte as colunas de data para strings, caso existam
    df.columns = [str(col) for col in df.columns]

    # Retorna a tabela Dash
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    )

# Callback para processar o upload e exibir a tabela
@app.callback(Output('output-table', 'children'),
              Input('upload-data', 'contents'))
def update_output(contents):
    if contents is not None:
        return parse_contents(contents)
    return html.Div("Faça o upload de um arquivo Excel para visualizar os dados.")


# Executa o app
if __name__ == '__main__':
    app.run_server(debug=True, port=8778)
