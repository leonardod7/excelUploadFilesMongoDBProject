# 0) Importando bibliotecas --------------------------------------------------------------------------------------------
from dash import dcc, html, Input, Output, State, callback, ALL, no_update, callback_context, dash_table
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
                                                      id='id-textarea-descricao-cenario',
                                                      placeholder="Descreva o cenário......",
                                                      w=1320,
                                                      autosize=True,
                                                      minRows=1,
                                                      maxRows=2,
                                                  ),
                                              ],
                                          )

                                      ]),

                                  # 3) Div - Upload Excel File
                                  html.Div(
                                      className="insert-doc-page-div-parametros-3",
                                      children=[
                                          html.H6(children=["Arraste e Solte o Arquivo Excel:"],
                                                  style={'fontWeight': 'bold', 'color': 'gray',
                                                         'fontFamily': 'Arial Narrow'}),
                                          dcc.Upload(
                                              id='id-upload-data',
                                              children=html.Div(
                                                  className='upload-excel-file',
                                                  children=[
                                                      html.A('Arraste e solte um arquivo Excel no formato permitido'),
                                                      html.Img(src='assets/img/excel_icon.png',
                                                               style={'width': '40px',
                                                                      'height': '40px',
                                                                      'margin-left': '10px'}),
                                                  ]),
                                              style={
                                                  'width': '50%',
                                                  'height': '60px',
                                                  'lineHeight': '60px',
                                                  'borderWidth': '1px',
                                                  'borderStyle': 'dashed',
                                                  'borderRadius': '5px',
                                                  'textAlign': 'center',
                                                  'margin': '10px auto',
                                                  'borderColor': 'black'
                                              },
                                              # Permite múltiplos arquivos
                                              multiple=False
                                          ),
                                      ]),

                                  # 3) Div - Botão para Salvar
                                  html.Div(
                                      className="insert-doc-page-div-parametros-4",
                                      children=[
                                          html.Button(
                                              className='btn-submit-doc',
                                              id='id-btn-submit-doc',
                                              children=['Salvar'], n_clicks=0)
                                      ]),

                                  # 4) Div - Output

                                  html.Div(id='id-div-output-save', children=[])
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

@callback(
    [Output(component_id='id-div-output-save', component_property='children'),
     Output(component_id='id-input-nome-usina', component_property='error'),
     Output(component_id='id-input-nome-cenario', component_property='error'),
     Output(component_id='id-textarea-descricao-cenario', component_property='error')],
    [State(component_id='id-radio-items-bancos-inserir-doc', component_property='value'),
     State(component_id='id-input-nome-usina', component_property='value'),
     State(component_id='id-input-nome-cenario', component_property='value'),
     State(component_id='id-radio-items-sheetname-inserir-doc', component_property='value'),
     State(component_id='id-textarea-descricao-cenario', component_property='value'),
     State(component_id='id-upload-data', component_property='contents')],
    Input(component_id='id-btn-submit-doc', component_property='n_clicks')
)
def get_info_file(banco, usina, cenario, sheetname, descricao, contents, n_clicks):
    if n_clicks > 0:

        error_usina = error_cenario = error_descricao = None

        # 1) Verificar se algum campo está vazio (None ou string vazia)
        if not all([banco, usina, cenario, sheetname, descricao]):
            if not usina:
                error_usina: str = "Nome da Usina não pode ser vazio!"
            if not cenario:
                error_cenario: str = "Nome do Cenário não pode ser vazio!"
            if not descricao:
                error_descricao: str = "Descrição do Cenário não pode ser vazio!"

            div_msg: html.Div = html.Div(children=["Erro: Preencha todos os campos obrigatórios!"],
                                         style={'color': 'red'})

            return div_msg, error_usina, error_cenario, error_descricao

        # 2) Verificar se o arquivo foi inserido
        if contents is None:
            msg: html.Div = html.Div(children=["Erro: Insira um arquivo Excel!"], style={'color': 'red'})
            return msg, None, None, None

        # 3) Tentar ler o arquivo e verificar as abas
        try:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            excel_data = pd.ExcelFile(io.BytesIO(decoded))

            # 3.1) Verificar se as abas necessárias estão presentes
            required_sheets = {"DRE", "FCD", "BP"}
            missing_sheets = required_sheets - set(excel_data.sheet_names)

            if missing_sheets:
                msg: html.Div = html.Div(
                    children=[f"Erro: O arquivo não contém as abas necessárias: {', '.join(missing_sheets)}."],
                    style={'color': 'red'}
                )
                return msg, None, None, None

            # 3.2) Se o arquivo e as abas estão corretos, montar o dicionário e salvar no banco
            df = parse_contents(contents)
            # TODO: PRECISAMOS PREPAR O ARQUIVO EXCEL PARA SALVAR NO BANCO DE DADOS

            # Exibir sucesso na interface e retornar os dados
            msg: html.Div = html.Div([
                html.P(children=["Arquivo inserido com sucesso!"], style={'color': 'green'}),
                # TODO: DEVEMOS USAR A TABELA FORMATADA CRIADA
                dash_table.DataTable(data=df.to_dict('records'), page_size=5)
            ])

            return msg, None, None, None

        except Exception as e:
            msg: html.Div = html.Div(children=[f"Erro ao processar o arquivo: {str(e)}"], style={'color': 'red'})
            return msg, None, None, None

    return no_update, None, None, None




# CALLBACK SEM A VALIDAÇÃO DE CAMPOS VAZIOS EM VERMELHO
# 1.3) Callback para identificar os inputs do banco, nome da usina, nome do cenário e sheetname:
# @callback(
#     Output(component_id='id-div-output-save', component_property='children'),
#     [State(component_id='id-radio-items-bancos-inserir-doc', component_property='value'),
#      State(component_id='id-input-nome-usina', component_property='value'),
#      State(component_id='id-input-nome-cenario', component_property='value'),
#      State(component_id='id-radio-items-sheetname-inserir-doc', component_property='value'),
#      State(component_id='id-textarea-descricao-cenario', component_property='value'),
#      State(component_id='id-upload-data', component_property='contents')],
#     Input(component_id='id-btn-submit-doc', component_property='n_clicks')
# )
# def get_info_file(banco, usina, cenario, sheetname, descricao, contents, n_clicks):
#     """
#     Função para identificar os inputs do banco, nome da usina, nome do cenário e sheetname
#     :param banco: Banco de Dados no Mongo DB Atlas
#     :param usina: Nome da Usina
#     :param cenario: Nome do Cenário
#     :param sheetname: Nome da Sheet
#     :param descricao: Descrição do Cenário
#     :param contents: Arquivo Excel
#     :param n_clicks: Número de cliques no botão
#     :return: Retorna um texto com as informações inseridas
#     """
#
#     if n_clicks > 0:
#
#         # 1) Verificar se algum campo está vazio (None ou string vazia)
#         if not all([banco, usina, cenario, sheetname, descricao]):
#
#             div_msg: html.Div = html.Div(children=["Erro: Preencha todos os campos!"], style={'color': 'red'})
#
#             return div_msg
#
#         # 2) Verificar se o arquivo foi inserido
#         if contents is None:
#             msg: html.Div = html.Div(children=["Erro: Insira um arquivo Excel!"], style={'color': 'red'})
#             return msg
#
#         # 3) Tentar ler o arquivo e verificar as abas
#         try:
#             content_type, content_string = contents.split(',')
#             decoded = base64.b64decode(content_string)
#             excel_data = pd.ExcelFile(io.BytesIO(decoded))
#
#             # 3.1) Verificar se as abas necessárias estão presentes
#             required_sheets = {"DRE", "FCD", "BP"}
#             missing_sheets = required_sheets - set(excel_data.sheet_names)
#
#             if missing_sheets:
#                 msg: html.Div = html.Div(
#                     children=[f"Erro: O arquivo não contém as abas necessárias: {', '.join(missing_sheets)}."],
#                     style={'color': 'red'}
#                 )
#                 return msg
#
#             # 3.2) Se o arquivo e as abas estão corretos, montar o dicionário
#             df = parse_contents(contents)
#             print(df)
#
#             # data_dict = {
#             #     "banco": banco,
#             #     "usina": usina,
#             #     "cenario": cenario,
#             #     "sheetname": sheetname,
#             #     "dados": df.to_dict(orient="records")  # Dados da aba escolhida
#             # }
#
#             # 3.3) Exibir sucesso na interface e retornar os dados
#             msg: html.Div = html.Div([
#                 html.P(children=["Arquivo inserido com sucesso!"], style={'color': 'green'}),
#                 dash_table.DataTable(data=df.to_dict('records'), page_size=5)
#             ])
#
#             return msg
#
#         except Exception as e:
#             msg: html.Div = html.Div(children=[f"Erro ao processar o arquivo: {e}"], style={'color': 'red'})
#             return msg
#
#     return no_update

# TODO: Antes de salvar o cenário, ele precisa mostrar em uma tela o que foi inserido, para o usuário confirmar
# TODO: Precisa existir uma verificação do nome do cenário, para não salvar cenários com o mesmo nome


# O uso de not all([banco_name, usina_name, cenario_name, sheet_name]) permite verificar se algum dos valores é
# None ou uma string vazia (''). Assim, a condição entrará no else apenas quando todos os campos estiverem preenchidos
