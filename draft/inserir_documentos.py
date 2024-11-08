# 0) Importando bibliotecas --------------------------------------------------------------------------------------------
from dash import dcc, html, Input, Output, State, callback, ALL, no_update, callback_context, dash_table
import pandas as pd
import dash_mantine_components as dmc
import json
import base64
import io


# Importando classes de conexão, funções e CRUD ------------------------------------------------------------------------
from dao.MongoCRUD_Teste import MongoDBCRUD
from model.MongoConnection import MongoEolicasConnection, MongoSolarConnection, MongoHidroConnection
from functions.funcoes import *


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
                                                      w=470,
                                                      placeholder="Nome da Usina",
                                                      # leftSection=DashIconify(icon="ic:round-alternate-email"),
                                                      style={'marginBottom': '20px'}
                                                  ),
                                                  html.H6(children=["Insira o nome do Cenário:"],
                                                          style={'fontWeight': 'bold', 'color': 'gray',
                                                                 'fontFamily': 'Arial Narrow'}),
                                                  dmc.TextInput(
                                                      id='id-input-nome-cenario',
                                                      w=470,
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
                                                      w=470,
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
                                          dcc.Upload(
                                              id='id-upload-data',
                                              children=html.Div(
                                                  className='upload-excel-file',
                                                  children=[
                                                      html.A('Arraste e solte um arquivo Excel no formato permitido'),
                                                      html.Img(src='assets/img/excel_icon.png',
                                                               style={'width': '30px',
                                                                      'height': '30px',
                                                                      'margin-left': '10px'}),
                                                  ]),
                                              style={
                                                  'width': '80%',
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
                                          dcc.ConfirmDialogProvider(
                                              children=[
                                                  html.Button(
                                                      className='btn-submit-doc',
                                                      id='id-btn-submit-doc',
                                                      children=['Salvar'], n_clicks=0)
                                              ],
                                              id='id-confirm-doc',
                                              message='Deseja salvar o cenário ?',
                                              submit_n_clicks=0)
                                      ]),

                                  # 4) Div - Output

                                  html.Div(id='id-div-output-save', children=[])
                              ])

    return page

# era antes de colocarmos o ConfirmDialogProvider: Input(component_id='id-btn-submit-doc',
# component_property='n_clicks')

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
    Input(component_id='id-confirm-doc', component_property='submit_n_clicks')
)
def get_info_file(banco, usina, cenario, sheetname, descricao, contents, n_clicks):
    """
    Função para identificar os inputs do banco, nome da usina, nome do cenário, nome das abas do arquivo Excel,
    descrição do cenário, arquivo Excel e número de cliques no botão
    :param banco:
    :param usina:
    :param cenario:
    :param sheetname:
    :param descricao:
    :param contents:
    :param n_clicks:
    :return:
    """

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
            df = parse_contents(contents=contents, sheetname=sheetname)
            print(df)  # debug
            # print(df.columns)



            # Até o print de cima, ambos estão iguais, o df usando na inserção manual e aqui

            # 3.2.1) Instanciando a classe de conexão com o banco de dados
            cliente = MongoSolarConnection() if banco == 'Solar' else MongoEolicasConnection() if banco == 'Eólicas' \
                else MongoHidroConnection()

            # 3.2.3) Criar as partes do documento    criar_partes_documento_from_drag_and_drop
            documentos: list[dict] = criar_partes_documento2(
                df=df,
                setor='hidro' if banco == 'Hidrelétricas' else 'eolicas' if banco == 'Eólicas' else 'solar',
                empresa_nome=usina,
                cenario_nome=cenario,
                descricao_cenario=descricao,
                sheet_name=sheetname,
                demonstrativo_name="Demonstração de Resultado" if sheetname == "DRE"
                else "Fluxo de Caixa Direto" if sheetname == "FCD" else "Balanço Patrimonial",
                nome_segunda_coluna="Driver"
            )

            # Verifique o conteúdo das variáveis chave
            # print(f"Banco: {banco}, Usina: {usina}, Cenario: {cenario}, Sheetname: {sheetname}, Descricao: {descricao}")

            if len(documentos) == 0:
                msg: html.Div = html.Div(children=["Erro: Nenhum documento foi gerado."], style={'color': 'red'})
                return msg, None, None, None

            # print(f"Documentos gerados: {documentos}")  # Verifique o conteúdo de 'documentos'
            if documentos is None:
                raise ValueError("A variável 'documentos' está com valor None.")

            crud = MongoDBCRUD(db_connection=cliente, collection_name=usina)
            doc_1 = documentos[0]
            print(doc_1)  # debug
            # unique_fields = {"empresa": usina, "nome": cenario, "tipo": sheetname}
            # crud.insert_document(document=doc_1, unique_fields=unique_fields)

            # for documento in documentos:
            #     # print(f"Processando documento: {documento}")  # Verifique cada documento antes de salvar
            #     unique_fields = {"empresa": usina, "nome": cenario, "tipo": sheetname}
            #     # print(unique_fields)  # debug
            #     crud.insert_document(document=documento, unique_fields=unique_fields)


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



    # # 3.2.4) CRUD para salvar os documentos no banco de dados
    # crud = MongoDBCRUD(db_connection=cliente, collection_name=collection_name)
    # doc_1 = documentos[0]
    # # print(doc_1)  # debug
    # unique_fields = {"empresa": collection_name, "nome": cenario_name, "tipo": sheet_name}
    # crud.insert_document(document=doc_1, unique_fields=unique_fields)

    # TODO: Tentamos resolver o problema achando que poderia ser o formato das datas, mas não era
    # df_2 = parse_contents(contents=contents, sheetname=sheetname)
    # def format_dates_from_third_column(df):
    #     # Itera sobre as colunas a partir da terceira (index 2)
    #     for col in df.columns[2:]:
    #         # Converte a coluna para o formato datetime
    #         df[col] = pd.to_datetime(df[col], errors='coerce')  # 'coerce' para tratar erros como NaT
    #     return df
    #
    # df_2 = format_dates_from_third_column(df=df_2)
    # print(df_2.columns)


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