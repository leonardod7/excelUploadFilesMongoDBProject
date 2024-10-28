from datetime import datetime

from bson import ObjectId
from datetime import datetime
from dash import dcc, html, Input, Output, State, callback, ALL, no_update, callback_context
from app import cache  # Importar o cache configurado
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from functions.agrupar_por_chave import agrupar_por_chave
from functions.funcoes import conectar_ao_banco, render_card, aplicar_formato_data
from functions.serealizar import json_serial, custom_json_decoder
import dash_mantine_components as dmc
import json
import copy


from functions.serealizar import dados_nao_serealizados

# 1) Dados iniciais das coleções ---------------------------------------------------------------------------------------
collection_eolicas_base_name: str = "SPE Ventos da Serra"
collection_solar_base_name: str = "Parque Solar 1"
collection_hidro_base_name: str = "UHE 1"


# Funções --------------------------------------------------------------------------------------------------------------

# Função para gerar a lista de cards -----------------------------------------------------------------------------------
def gerar_lista_cards(agrupado_formatado: dict[list[dict]],
                      agrupado_formatado_cenarios: dict[list[dict]]) -> list[html.Div]:
    cards = []

    for grupo, itens in agrupado_formatado.items():
        # print(grupo)  # debug Cenário 1, Cenário 2, etc

        div: html.Div = html.Div(children=[
            # Div com o título do grupo
            dmc.Stack([
                dmc.Divider(label=grupo,
                            color="lightgray",
                            labelPosition="left",
                            size="md",
                            style={
                                'fontWeight': 'bold',
                                'fontFamily': 'Arial Narrow',
                                'fontSize': '16px',
                                'marginTop': '10px',
                                'marginBottom': '10px',
                                'color': 'gray',
                            })]),

            # Div com o botão de exclusão
            html.Div([
                dbc.Button(children=["🗑️"], n_clicks=0,
                           className="delete-button-cenarios",
                           id={"type": "delete-btn", "index": grupo}
                           ),
            ]),

            # Div com os cards
            html.Div([render_card(cenario=item) for item in itens], style={'display': 'flex',
                                                                           'flexDirection': 'column',
                                                                           # 'border': '1px solid gold',
                                                                           'padding': '10px',
                                                                           'marginBottom': '10px', })
        ], style={
            'border': '1px solid red',
            'marginBottom': '10px',
        })
        # print(grupo)  # debug Cenário 1, Cenário 2, etc
        # print(itens)  # debug Lista com os dicionários dos cenários parte 1, 2, 3, 4.
        cards.append(div)  # Título do grupo

    return cards


def criar_cenarios(dicionario: dict[list[dict]]) -> dict[dict:list[dict]]:
    # Criar um novo dicionário com a chave "Cenários"
    cenarios = {"Cenários": dicionario}
    return cenarios


def json_deserial(data):
    # Verifica se 'data' é um dicionário que contém cenários
    if isinstance(data, dict) and 'Cenários' in data:
        for cenario, documentos in data['Cenários'].items():
            # Verifica se 'documentos' é uma lista
            if isinstance(documentos, list):
                for doc in documentos:
                    for key, value in doc.items():
                        # Converte strings que representam ObjectId de volta ao formato ObjectId
                        if key == '_id' and isinstance(value, str):
                            doc[key] = ObjectId(value)
                        # Converte strings ISO de volta para datetime
                        elif isinstance(value, str) and 'T' in value and ':' in value:
                            try:
                                doc[key] = datetime.fromisoformat(value)
                            except ValueError:
                                pass  # Ignora erros de conversão
    return data


def stringify_object_ids(data):
    for cenario, docs in data.items():
        for doc in docs:
            if '_id' in doc and isinstance(doc['_id'], ObjectId):
                doc['_id'] = str(doc['_id'])
    return data


# 2) Página de consultar documentos ------------------------------------------------------------------------------------
def consultar_documentos_page():
    page: html.Div = html.Div(
        id="id-upload-section-page",
        className="consult-section-page",
        children=[

            # Div - 0 -------------------------------------------------------------------------------------------
            html.Div(
                className="consult-section-page-0",
                children=[

                ]),

            # Div - 1 -------------------------------------------------------------------------------------------
            html.Div(
                className="consult-section-page-1",
                children=[
                    html.H6(children=["Escolha o Banco de Dados no Mongo DB Atlas:"],
                            style={'fontWeight': 'bold', 'color': 'gray', 'fontFamily': 'Arial Narrow'}),
                    dcc.RadioItems(
                        id='id-radio-items-bancos',
                        className="custom-radio-items",
                        options=[
                            {'label': html.Span(children=[
                                html.Img(src='/assets/img/db_cinza.png',
                                         style={'width': '20px', 'height': '20px', 'marginRight': '10px'}),
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
                                         style={'width': '20px', 'height': '20px', 'marginRight': '10px'}),
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
                                         style={'width': '20px', 'height': '20px', 'marginRight': '10px'}),
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
            # Div - 2 -------------------------------------------------------------------------------------------
            html.Div(
                # Div azul ---------------------------------------------------------------------------------------
                className="consult-section-page-2",
                children=[
                    # Div rosa ---------------------------------------------------------------------------------------
                    html.Div(className="consult-section-page-2-1",
                             children=[
                                 html.H6(children=["Escolha a Coleção de Dados:"],
                                         style={'fontWeight': 'bold', 'color': 'gray', 'fontFamily': 'Arial Narrow'}),
                                 html.Div(id="id-div-colecoes", children=[]),
                             ]),
                    # Div preta --------------------------------------------------------------------------------------
                    html.Div(className="consult-section-page-2-2",
                             children=[
                                 html.Div(className="consult-section-page-2-2-1",
                                          id="id-consult-section-page-2-2-1",
                                          children=[]),
                             ]
                             )
                ],
            ),
            # Div 3 ------------------------------------------------------------------------------------------------
            # TODO: teste para receber uma selecao de documentos

        ])

    return page


# 3) Callbacks ---------------------------------------------------------------------------------------------------------

# 3.1) Callback para fazer upload da coleção selecionada e enviar para o dcc.Store -------------------------------------
@callback(
    Output(component_id='id-cenarios-store', component_property='data'),
    Output(component_id='id-collection-db_names-store', component_property='data'),
    [Input(component_id='id-radio-items-bancos', component_property='value'),  # Input para o banco de dados
     Input(component_id='id-div-colecoes', component_property='children'),  # Input para as coleções
     Input(component_id='id-colecoes-radio', component_property='value')],
)
def upload_data_from_mongo_to_store(db_name, colecoes_div, collection):

    collection_db_names = [db_name, collection]
    # print(collection_db_names)  # debug

    if collection:

        # 1) Vamos listar todos os documentos presentes em collection
        filtro: dict = {"empresa": collection}
        projecao = {"_id": 1, "nome": 1, "descricao": 1, "data": 1, "empresa": 1, "tipo": 1, "parte": 1, "setor": 1}

        # 2) Conectar ao banco de dados e buscar documentos
        cliente, crud = conectar_ao_banco(collection_name=collection, database_name=db_name)

        try:
            response: list[dict] = crud.select_many_documents(query=filtro, projection=projecao)
            print('response')
            print(response)
            # 1.2) Agrupando lista de dicionarios por nome
            agrupado = agrupar_por_chave(lista=response, chave="nome")

            # 1.3) Cria dicionário para ser utilizado na estrutura do dcc.Store
            cenarios: dict[dict:list[dict]] = criar_cenarios(agrupado)

            # 1.4) Converte dicionário em JSON para ser armazenado em um dcc.Store
            json_cenarios = json.dumps(cenarios, default=str)  # Dados que serão armazenados no dcc.Store

            # print('json data armazenado no dcc.Store: id-cenarios-store')  # debug
            # print(json_cenarios)  # debug

        finally:
            cliente.close_connection()

    else:
        return "Nenhuma coleção selecionada."

    return json_cenarios, collection_db_names


# 3.2) Callback para listar apenas o nome das coleções com cache com Radio Items ---------------------------------------
@callback(
    Output(component_id='id-div-colecoes', component_property='children'),
    Input(component_id='id-radio-items-bancos', component_property='value')
)
def listar_colecoes_radio_items(value):
    if value == 'Eólicas':

        # Nome da coleção no cache
        colecao_name: str = 'eolicas_colecoes'
        # Verifica se as coleções já estão no cache
        colecoes = cache.get(colecao_name)

        if not colecoes:
            # Se não estiverem no cache, acessa o banco de dados
            cliente, eolicas_crud = conectar_ao_banco(collection_name=collection_eolicas_base_name,
                                                      database_name=value)
            try:
                colecoes = eolicas_crud.list_collections()
                cache.set(colecao_name, colecoes)  # Armazena no cache
            finally:
                cliente.close_connection()  # Fecha a conexão ao banco de dados

        # Cria RadioItems dinamicamente com as coleções retornadas
        radio_items = [{'label': html.Span([html.Img(style={'width': '20px', 'height': '20px', 'marginRight': '10px'},
                                                     src='/assets/img/database.png'), collection]),
                        'value': collection} for collection in colecoes]

        dc_radio_eolicas: dcc.RadioItems = dcc.RadioItems(id='id-colecoes-radio',  # id-colecoes-radio-eolicas
                                                          className="custom-radio-items",
                                                          options=radio_items,
                                                          value=radio_items[0]['value'] if radio_items else None,
                                                          style={
                                                              'fontWeight': 'bold',
                                                              'fontFamily': 'Arial Narrow',
                                                              'fontSize': '14px',
                                                          })

        return dc_radio_eolicas

    elif value == 'Solar':

        # Nome da coleção no cache
        colecao_name: str = 'solar_colecoes'
        # Verifica se as coleções já estão no cache
        colecoes = cache.get(colecao_name)

        if not colecoes:
            # Se não estiverem no cache, acessa o banco de dados
            cliente, solar_crud = conectar_ao_banco(collection_name=collection_solar_base_name,
                                                    database_name=value)
            try:
                colecoes = solar_crud.list_collections()
                cache.set(colecao_name, colecoes)  # Armazena no cache
            finally:
                cliente.close_connection()

        # Cria RadioItems dinamicamente com as coleções retornadas
        radio_items = [{'label': html.Span([html.Img(style={'width': '20px', 'height': '20px', 'marginRight': '10px'},
                                                     src='/assets/img/database.png'), collection]),
                        'value': collection} for collection in colecoes]

        dc_radio_solar: dcc.RadioItems = dcc.RadioItems(id='id-colecoes-radio',  # id-colecoes-radio-solar
                                                        className="custom-radio-items",
                                                        options=radio_items,
                                                        value=radio_items[0]['value'] if radio_items else None,
                                                        style={
                                                            'fontWeight': 'bold',
                                                            'fontFamily': 'Arial Narrow',
                                                            'fontSize': '14px',
                                                        })

        return dc_radio_solar

    elif value == 'Hidrelétricas':

        # Nome da coleção no cache
        colecao_name: str = 'hidro_colecoes'
        # Verifica se as coleções já estão no cache
        colecoes = cache.get(colecao_name)

        if not colecoes:
            # Se não estiverem no cache, acessa o banco de dados
            cliente, hidro_crud = conectar_ao_banco(collection_name=collection_hidro_base_name,
                                                    database_name=value)
            try:
                colecoes = hidro_crud.list_collections()
                cache.set(colecao_name, colecoes)  # Armazena no cache
            finally:
                cliente.close_connection()

        # Cria RadioItems dinamicamente com as coleções retornadas
        radio_items = [{'label': html.Span([html.Img(style={'width': '20px', 'height': '20px', 'marginRight': '10px'},
                                                     src='/assets/img/database.png'), collection]),
                        'value': collection} for collection in colecoes]

        dc_radio_hidro: dcc.RadioItems = dcc.RadioItems(id='id-colecoes-radio',  # id-colecoes-radio-hidro
                                                        className="custom-radio-items",
                                                        options=radio_items,
                                                        value=radio_items[0]['value'] if radio_items else None,
                                                        style={
                                                            'fontWeight': 'bold',
                                                            'fontFamily': 'Arial Narrow',
                                                            'fontSize': '14px',
                                                        })

        return dc_radio_hidro


# 3.3) Callback para atualizar os cards com base nos dados -------------------------------------------------------------
@callback(
    Output(component_id="id-consult-section-page-2-2-1", component_property="children"),
    Input(component_id="id-cenarios-store", component_property="data")
)
def mostrar_cards_colecoes(cenarios: dict[dict:list[dict]]):
    # Verifica se 'cenarios' é None, e se for, interrompe o callback
    if cenarios is None:
        return no_update  # Mantém o estado anterior sem atualizar

    try:
        data_store = json.loads(cenarios)
        data_final: dict[dict:list[dict]] = json_deserial(data_store)  # Dados que serão utilizados
        data_final_cenarios: dict[list[dict]] = data_final['Cenários']

        # print('Cenários Store: ')  # debug
        # print(cenarios)  # debug
        # print('Agrupado formatado: ')  # debug
        # print(data_final)  # debug
        # print('Data Final Cenários: ')  # debug
        # print(data_final_cenarios)  # debug

        cards: list[html.Div] = gerar_lista_cards(agrupado_formatado=data_final_cenarios,
                                                  agrupado_formatado_cenarios=data_final)
    except json.JSONDecodeError:
        return "Nenhum dado disponível para renderização."

    return cards


# 3.4) Callback para deletar um documento do banco de dados ------------------------------------------------------------
# Vamos excluir os documentos com base nos ids que pertencem a um mesmo cenário
@callback(Output(component_id="id-cenarios-store", component_property="data", allow_duplicate=True),
          Input(component_id={"type": "delete-btn", "index": ALL}, component_property="n_clicks"),
          State(component_id="id-collection-db_names-store", component_property="data"),
          State(component_id="id-cenarios-store", component_property="data"), prevent_initial_call=True)
def deletar_documento(n_clicks, list_banco_collection, data):

    # print('Debug: -----')
    # print('Data: -------------------------------------------------------------------------------------------- debug')
    # print(data)

    banco_nome = list_banco_collection[0]
    colecao_nome = list_banco_collection[1]

    print('Coleção: ', banco_nome)
    print('Bancos: ', colecao_nome)

    # 1) Obter o contexto do callback para verificar qual entrada foi acionada
    ctx = callback_context
    triggered = ctx.triggered[0]['prop_id'].split('.')[0]
    print('Triggered context: ', triggered)
    # {"index":"Cenário 2","type":"delete-button"} ou {"index":"Cenário 1","type":"delete-button"}

    # 2) Se o callback foi acionado pelo radio items dos bancos, não faz nada

    if not ctx.triggered or not n_clicks or all(click is None for click in n_clicks):
        raise PreventUpdate

    print('n clicks:', n_clicks)
    total_clicks = sum(n_clicks)

    # 3) Se o callback foi acionado pelo botão de deletar, processa a atualização. o n_clicks precisa ser maior que 0
    if total_clicks > 0:
        # 3.1) Identifica o botão clicado com o nome da chave (Cenário 1, Cenário 2 etc)
        btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
        print('btn_id: ', btn_id)  # {'index': 'Cenário 1', 'type': 'delete-btn'}
        btn_id = eval(btn_id)  # Converte a string de volta ao dicionário para podermos acessar os valores separadamente
        btn_id_type = btn_id['type']  # delete-btn
        cenario_nome = btn_id['index']  # Cenário 1, 2, e etc..
        print('btn_id_type: ', btn_id_type)
        print('Cenário Nome: ', cenario_nome)

    # TODO: Até aqui a parte de cima, está ok.

        # 3.2.1) Vamos importar os dados do dcc.Store
        data_store = json.loads(data)
        print('Data Store: ', data_store)

        # 3.2.2) Desserializar os dados
        data_final: dict[dict:list[dict]] = json_deserial(data_store)
        print('Data Final: ', data_final)

        # 3.2.3) Vamos criar um dicionário com o nome das chaves e seus respectivos ids
        dict_ids = {}
        for cenario, docs in data_final['Cenários'].items():
            dict_ids[cenario] = [doc['_id'] for doc in docs]
        print('Dict IDs: ', dict_ids)

        # 3.2.4) Conectar ao banco de dados
        banco_name = banco_nome
        colecao_name = colecao_nome
        cliente, crud = conectar_ao_banco(collection_name=colecao_name, database_name=banco_name)

        # 3.2.5) Deletar os documentos dentro do dicionario
        cenario_selecionado = dict_ids[cenario_nome]
        print('Cenário Selecionado', cenario_selecionado)

        for id_ in cenario_selecionado:
            filtro = {"_id": id_}
            crud.delete_one_document(query=filtro)

        # 3.2.6) Fechar a conexão
        cliente.close_connection()

        # TODO: Até aqui a parte de cima, está ok. Estamos conseguindo deletar os documentos com base nos ids do cenário.

        # 3.2.7) Precisamos agora deletar todos os documentos que foram deletados no banco, do data_final para que
        # possamos atualizar o dcc.Store

        data_final_copy = copy.deepcopy(data_final)

        if cenario_nome in data_final_copy['Cenários']:
            del data_final_copy['Cenários'][cenario_nome]

        # 3.2.8) Converte dicionário em JSON para ser devolvido ao dcc.Store
        json_cenarios = json.dumps(data_final_copy, default=str)  # Dados que serão armazenados no dcc.Store

        return json_cenarios

    return data

# TODO: PRECISAMOS INCLUIR UM AJUSTE PARA CONSEGUIR INCLUIR A DRE, O BP E O FCD NO MESMO CENÁRIO NOME. ESSE AJUSTE É
# NA INSERÇÃO ONDE VERÁ LEVAR EM CONSIDERAÇÃO O TIPO DE DOCUMENTO QUE ESTÁ SENDO INSERIDO. SE FOR DRE, BP OU FCD,


