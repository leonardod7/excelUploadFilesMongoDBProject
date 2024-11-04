# 0) Importando bibliotecas --------------------------------------------------------------------------------------------
from dash import dcc, html, Input, Output, State, callback, ALL, no_update, callback_context
import pandas as pd
import base64
import io
import dash_mantine_components as dmc


# 1) Criando página de inserção de documentos --------------------------------------------------------------------------

# 1.1) Criando a página de inserção de documentos
def inserir_documentos_page():
    page: html.Div = html.Div(className="insert-doc-page",
                              children=[
                                  # 1) Div - Parâmetros (Setor, Usina, Sheetname)
                                  html.Div(
                                      className="insert-doc-page-div-parametros-1",
                                      children=[
                                          # 1.1) Div - Escolha o Banco de Dados no Mongo DB Atlas
                                          html.Div(
                                              className="insert-section-page-1",
                                              children=[
                                                  html.H6(children=["Escolha o Banco de Dados no Mongo DB Atlas:"],
                                                          style={'fontWeight': 'bold', 'color': 'gray',
                                                                 'fontFamily': 'Arial Narrow'}),
                                                  dcc.RadioItems(
                                                      id='id-radio-items-bancos-inserir-doc',
                                                      className="custom-radio-items",
                                                      options=[
                                                          {'label': html.Span(children=[
                                                              html.Img(src='/assets/img/db_cinza.png',
                                                                       style={'width': '20px', 'height': '20px',
                                                                              'marginRight': '10px'}),
                                                              "Eólicas"
                                                          ], style={
                                                              'fontWeight': 'bold',
                                                              'fontFamily': 'Arial Narrow',
                                                              'fontSize': '14px',
                                                          }),
                                                              'value': 'Eólicas'
                                                          },
                                                          {'label': html.Span(children=[
                                                              html.Img(src='/assets/img/db_cinza.png',
                                                                       style={'width': '20px', 'height': '20px',
                                                                              'marginRight': '10px'}),
                                                              "Solar"
                                                          ], style={
                                                              'fontWeight': 'bold',
                                                              'fontFamily': 'Arial Narrow',
                                                              'fontSize': '14px',
                                                          }),
                                                              'value': 'Solar'
                                                          },
                                                          {'label': html.Span(children=[
                                                              html.Img(src='/assets/img/db_cinza.png',
                                                                       style={'width': '20px', 'height': '20px',
                                                                              'marginRight': '10px'}),
                                                              "Hidrelétricas"
                                                          ], style={
                                                              'fontWeight': 'bold',
                                                              'fontFamily': 'Arial Narrow',
                                                              'fontSize': '14px',
                                                          }),
                                                              'value': 'Hidrelétricas'
                                                          }
                                                      ], value='Eólicas'),
                                              ]),

                                          # 1.2) Div - Insira o nome da usina (coleção)
                                          html.Div(
                                              className="insert-section-page-2",
                                              children=[
                                                  html.H6(children=["Insira o nome da usina (coleção):"],
                                                          style={'fontWeight': 'bold', 'color': 'gray',
                                                                 'fontFamily': 'Arial Narrow'}),
                                                  dmc.TextInput(
                                                      id='id-input-nome-usina',
                                                      w=360,
                                                      placeholder="Nome da Usina",
                                                      error="Message can't be empty!",
                                                      # leftSection=DashIconify(icon="ic:round-alternate-email"),
                                                      style={'marginBottom': '20px'}
                                                  ),
                                                  html.H6(children=["Insira o nome do Cenário:"],
                                                          style={'fontWeight': 'bold', 'color': 'gray',
                                                                 'fontFamily': 'Arial Narrow'}),

                                                  dmc.TextInput(
                                                      id='id-input-nome-cenario',
                                                      w=360,
                                                      placeholder="Nome do Cenário",
                                                      error="Message can't be empty!",
                                                      # leftSection=DashIconify(icon="ic:round-alternate-email"),
                                                  )


                                              ]),

                                          # 1.3) Div - Nome da sheet
                                          html.Div(
                                              className="insert-section-page-3",
                                              children=[
                                                  html.H6(children=["Escolha o Nome da Sheet:"],
                                                          style={'fontWeight': 'bold', 'color': 'gray',
                                                                 'fontFamily': 'Arial Narrow'}),
                                                  dcc.RadioItems(
                                                      id='id-radio-items-sheetname-inserir-doc',
                                                      className="custom-radio-items",
                                                      options=[
                                                          {'label': html.Span(children=[
                                                              html.Img(src='/assets/img/excel_icon.png',
                                                                       style={'width': '20px', 'height': '20px',
                                                                              'marginRight': '10px'}),
                                                              "DRE"
                                                          ], style={
                                                              'fontWeight': 'bold',
                                                              'fontFamily': 'Arial Narrow',
                                                              'fontSize': '14px',
                                                          }),
                                                              'value': 'DRE'
                                                          },
                                                          {'label': html.Span(children=[
                                                              html.Img(src='/assets/img/excel_icon.png',
                                                                       style={'width': '20px', 'height': '20px',
                                                                              'marginRight': '10px'}),
                                                              "FCD"
                                                          ], style={
                                                              'fontWeight': 'bold',
                                                              'fontFamily': 'Arial Narrow',
                                                              'fontSize': '14px',
                                                          }),
                                                              'value': 'FCD'
                                                          },
                                                          {'label': html.Span(children=[
                                                              html.Img(src='/assets/img/excel_icon.png',
                                                                       style={'width': '20px', 'height': '20px',
                                                                              'marginRight': '10px'}),
                                                              "BP"
                                                          ], style={
                                                              'fontWeight': 'bold',
                                                              'fontFamily': 'Arial Narrow',
                                                              'fontSize': '14px',
                                                          }),
                                                              'value': 'BP'
                                                          }
                                                      ], value='DRE'),
                                              ]),

                                      ]),

                                  # 2) Div - Descrição do cenário
                                  html.Div(
                                      className="insert-doc-page-div-parametros-2",
                                      children=[
                                          html.H6(children=["Descreva o Cenário que será Salvo:"],
                                                  style={'fontWeight': 'bold', 'color': 'gray',
                                                         'fontFamily': 'Arial Narrow'}),
                                          dmc.Stack(
                                              children=[
                                                  dmc.Textarea(
                                                      placeholder="Descreva o cenário......",
                                                      w=1320,
                                                      autosize=True,
                                                      minRows=1,
                                                      maxRows=2,
                                                      error="Message can't be empty!",
                                                  ),
                                              ],
                                          )

                                      ]),

                                  # Upload Excel File
                                  html.Div(
                                      className="insert-doc-page-div-parametros-3",
                                      children=[
                                          html.H6(children=["Arraste e Solte o Arquivo Excel:"],
                                                  style={'fontWeight': 'bold', 'color': 'gray',
                                                         'fontFamily': 'Arial Narrow'}),
                                          ])

                                  #
                                  # html.H5("Inserir Documentos"),
                                  #
                                  #   # 1.1.2) Upload de arquivos
                                  #   dcc.Upload(
                                  #       id='upload-data',
                                  #       children=html.Div(
                                  #           className='upload-excel-file',
                                  #           children=[
                                  #               html.A('Arraste e solte um arquivo Excel no formato permitido'),
                                  #               html.Img(src='assets/img/excel_icon.png', style={'width': '40px',
                                  #                                                                'height': '40px',
                                  #                                                                'margin-left': '10px'}),
                                  #       ]),
                                  #       style={
                                  #           'width': '50%',
                                  #           'height': '60px',
                                  #           'lineHeight': '60px',
                                  #           'borderWidth': '1px',
                                  #           'borderStyle': 'dashed',
                                  #           'borderRadius': '5px',
                                  #           'textAlign': 'center',
                                  #           'margin': '10px auto',
                                  #           'borderColor': 'black'
                                  #       },
                                  #       # Permite múltiplos arquivos
                                  #       multiple=False
                                  #   ),
                                  #
                                  #   # 1.1.3) Tabela para exibir as 10 primeiras linhas
                                  #   html.Div(id='output-table')

                              ])

    return page


# 1.2) Função para ler o arquivo Excel e gerar um DataFrame
def parse_contents(contents: str):
    """
    Função para ler o arquivo Excel e gerar um DataFrame
    :param contents: contents é uma string codificada em Base64, que contém o arquivo Excel
    :return: Retorna um dataframe
    """
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
    return df
