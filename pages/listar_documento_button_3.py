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
                           id={"type": "delete-button", "index": grupo}
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
            html.Div(
                className="consult-section-page-3",
                children=[
                    html.Div(id="id-teste", children=[], style={
                        'marginTop': '20px',
                        'border': '1px solid red',
                    }),
                ]
            )
        ])

    return page


# 3) Callbacks ---------------------------------------------------------------------------------------------------------

# 3.1) Callback para fazer upload da coleção selecionada e enviar para o dcc.Store -------------------------------------
@callback(
    Output(component_id='id-cenarios-store', component_property='data'),
    [Input(component_id='id-radio-items-bancos', component_property='value'),  # Input para o banco de dados
     Input(component_id='id-div-colecoes', component_property='children'),  # Input para as coleções
     Input(component_id='id-colecoes-radio', component_property='value')],  # State para coleção de Eólicas
)
def upload_data_from_mongo_to_store(db_name, colecoes_div, collection):
    if collection:

        # 1) Vamos listar todos os documentos presentes em collection
        filtro: dict = {"empresa": collection}
        projecao = {"_id": 1, "nome": 1, "descricao": 1, "data": 1, "empresa": 1, "tipo": 1, "parte": 1, "setor": 1}

        # 2) Conectar ao banco de dados e buscar documentos
        cliente, crud = conectar_ao_banco(collection_name=collection, database_name=db_name)

        try:
            response: list[dict] = crud.select_many_documents(query=filtro, projection=projecao)
            # print('response')
            # print(response)
            # 1.2) Agrupando lista de dicionarios por nome
            agrupado = agrupar_por_chave(lista=response, chave="nome")

            # 1.3) Cria dicionário para ser utilizado na estrutura do dcc.Store
            cenarios: dict[dict:list[dict]] = criar_cenarios(agrupado)

            # 1.4) Converte dicionário em JSON para ser armazenado em um dcc.Store
            json_cenarios = json.dumps(cenarios, default=str)  # Dados que serão armazenados no dcc.Store

            print('json data armazenado no dcc.Store: id-cenarios-store')  # debug
            print(json_cenarios)  # debug

        finally:
            cliente.close_connection()

    else:
        return "Nenhuma coleção selecionada."

    return json_cenarios


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

    else:

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
    data_store = json.loads(cenarios)
    data_final: dict[dict:list[dict]] = json_deserial(data_store)  # Dados que serão utilizados
    data_final_cenarios: dict[list[dict]] = data_final['Cenários']

    # print('Agrupado formatado: ')
    # print(data_final)
    # print('Cenários: ')
    # print(data_final_cenarios)

    cards: list[html.Div] = gerar_lista_cards(agrupado_formatado=data_final_cenarios,
                                              agrupado_formatado_cenarios=data_final)

    return cards


# 3.4) Callback para deletar um documento do banco de dados ------------------------------------------------------------
# Vamos excluir os documentos com base nos ids que pertencem a um mesmo cenário
@callback(Output(component_id="id-cenarios-store", component_property="data", allow_duplicate=True),
          Input(component_id={"type": "delete-button", "index": ALL}, component_property="n_clicks"),
          State(component_id="id-cenarios-store", component_property="data"),
          prevent_initial_call=True)
def deletar_documento(n_clicks, data):

    # print('Debug: -----')
    # print('Data: ----- debug')
    # print(data)

    # 1) Vamos importar os dados do dcc.Store
    data_store = json.loads(data)

    # 2) Desserializar os dados
    data_final: dict[dict:list[dict]] = json_deserial(data_store)  # Dados que serão utilizados
    # print(data_final)

    # 3) Vamos criar um dicionário com o nome das chaves e seus respectivos ids
    dict_ids = {}
    for cenario, docs in data_final['Cenários'].items():
        dict_ids[cenario] = [doc['_id'] for doc in docs]


    # 4) Vamos verificar qual botão foi clicado e a qual chave ele pertence. Com base nessa chave,
    # vamos deletar todos os documentos que que estão associados a ela no dict ids
    ctx = callback_context
    if not ctx.triggered or not n_clicks or all(click is None for click in n_clicks):
        raise PreventUpdate

    # Identifica o botão clicado com o nome da chave (Cenário 1, Cenário 2 etc)
    btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
    # print('btn_id: ', btn_id)  # btn_id:  {"index":"Cenário 1","type":"delete-button"}
    btn_id = eval(btn_id)  # Converte a string de volta ao dicionário
    # print('btn_id: ', btn_id)  # {'index': 'Cenário 1', 'type': 'delete-button'}

    cenario_nome = btn_id['index']
    print('Cenário Nome: ', cenario_nome)  # Cenário Nome:  Cenário 1

    # TODO: o código abaixo está quase 200%. Precisamos apenas incluir o banco e coleção de forma automáticas.
    # # 5) Vamos deletar todos os documentos que estão associados a essa chave. Vamos acessar primeiro para cada id do
    # # cenario selecionado, rodaremos um delete no mongo db
    #
    # # 5.1) Conectar ao banco de dados
    #
    # banco_name = ""
    # colecao_name = ""
    # cliente, crud = conectar_ao_banco(collection_name=colecao_name, database_name=banco_name)
    #
    # # 5.2) Deletar os documentos
    # for id_ in dict_ids[cenario_nome]:
    #     filtro = {"_id": id_}
    #     crud.delete_one_document(filtro)
    #
    # # 5.3) Fechar a conexão
    # cliente.close_connection()
    #
    # # 6) Precisamos agora deletar todos os documentos com os ids que estão associados a essa chave do data_final
    #
    # # 6.1) Vamos deletar a chave do dicionário
    # data_final_copy = data_final.copy()
    #
    # if cenario_nome in data_final_copy['Cenários']:
    #     del data_final_copy['Cenários'][cenario_nome]
    #
    # # 6.2) Vamos retornar os dados atualizados
    #
    # return data_final_copy

    return None














    # ctx = callback_context
    # if not ctx.triggered:
    #     raise PreventUpdate
    #
    # # Identifica o botão clicado
    # btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
    # btn_id = eval(btn_id)  # Converte a string de volta ao dicionário
    #
    # # Remove o cenário correspondente ao botão clicado
    # cenario_nome = btn_id['index']
    # if cenario_nome in data_final:
    #     del data_final[cenario_nome]

    # Retorna o layout atualizado e o novo estado do dcc.Store
    return None


# TODO: no momento de inserção de documentos, deveremos ter uma verificação para ver se já existe um cenário com o mesmo
#  nome que está sendo inserido. Se existir, uma mensagem de alerta é mostrada para o usuário pedindo para ele
#  renomear o cenário. Se ele não renomear, não será possível inserir o cenário.

# TODO: Os documentos dos cenários agora pertence a uma chave chama "Cenários". Dentro dessa chave, temos os cenários (Cenário 1, Cenário 2 etc).
# TODO: Precisamos pensar na lógica agora de ao apertar o botão de deletar, ele identificar a qual cenário foi clicado e deletar todos os documentos
# Delete: nosso botão de delete terá um id: id={"type": "delete-button", "index": agrupado_formatado['Cenários']}


# Executar o app
if __name__ == "__main__":
    colecao = "SPE Ventos da Serra"
    cliente, crud = conectar_ao_banco(collection_name=colecao, database_name="Eólicas")
    # print(crud.list_collections())  # debug
    filtro: dict = {"empresa": colecao}
    projecao = {"_id": 1, "nome": 1, "descricao": 1, "data": 1, "empresa": 1, "tipo": 1, "parte": 1, "setor": 1}
    response: list[dict] = crud.select_many_documents(query=filtro, projection=projecao)

    print(response)  # debug

    # agrupado = agrupar_por_chave(lista=response, chave="nome")
    # # Debug agrupado --------------------------------------------------------------------------------------------------
    # print(agrupado)

    agrupado_formatado: dict[list[dict]] = {'Cenário 2':
        [
            {'_id': ObjectId('67111516808999e3b2900018'),
             'nome': 'Cenário 2',
             'descricao': 'Cenário de venda de parques solares + 5%',
             'data': '17/10/2024 10:45:57',
             'setor': 'solar',
             'empresa': 'Parque Solar 1',
             'tipo': 'dre',
             'parte': 1},
            {'_id': ObjectId('67111516808999e3b2900019'),
             'nome': 'Cenário 2',
             'descricao': 'Cenário de venda de parques solares + 5%',
             'data': '17/10/2024 10:45:57',
             'setor': 'solar',
             'empresa': 'Parque Solar 1',
             'tipo': 'dre',
             'parte': 2},
            {'_id': ObjectId('67111516808999e3b290001a'),
             'nome': 'Cenário 2',
             'descricao': 'Cenário de venda de parques solares + 5%',
             'data': '17/10/2024 10:45:57',
             'setor': 'solar',
             'empresa': 'Parque Solar 1',
             'tipo': 'dre',
             'parte': 3},
            {'_id': ObjectId('67111516808999e3b290001b'),
             'nome': 'Cenário 2',
             'descricao': 'Cenário de venda de parques solares + 5%',
             'data': '17/10/2024 10:45:58',
             'setor': 'solar',
             'empresa': 'Parque Solar 1',
             'tipo': 'dre',
             'parte': 4}
        ],
        'Cenário 1': [
            {'_id': ObjectId('6711153207ea80384ddb82e5'),
             'nome': 'Cenário 1',
             'descricao': 'Cenário de venda de parques solares + 5%',
             'data': '17/10/2024 10:46:25',
             'setor': 'solar',
             'empresa': 'Parque Solar 1',
             'tipo': 'dre',
             'parte': 1},
            {'_id': ObjectId('6711153207ea80384ddb82e6'),
             'nome': 'Cenário 1',
             'descricao': 'Cenário de venda de parques solares + 5%',
             'data': '17/10/2024 10:46:25',
             'setor': 'solar',
             'empresa': 'Parque Solar 1',
             'tipo': 'dre',
             'parte': 2},
            {'_id': ObjectId('6711153207ea80384ddb82e7'),
             'nome': 'Cenário 1',
             'descricao': 'Cenário de venda de parques solares + 5%',
             'data': '17/10/2024 10:46:25',
             'setor': 'solar',
             'empresa': 'Parque Solar 1',
             'tipo': 'dre',
             'parte': 3},
            {'_id': ObjectId('6711153207ea80384ddb82e8'),
             'nome': 'Cenário 1',
             'descricao': 'Cenário de venda de parques solares + 5%',
             'data': '17/10/2024 10:46:25',
             'setor': 'solar',
             'empresa': 'Parque Solar 1',
             'tipo': 'dre',
             'parte': 4},
            {'_id': ObjectId('6711158485d1d4c8dfd8fce3'),
             'nome': 'Cenário 1',
             'descricao': 'Cenário de venda de parques solares + 5%',
             'data': '17/10/2024 10:47:48',
             'setor': 'solar',
             'empresa': 'Parque Solar 1',
             'tipo': 'bp',
             'parte': 1},
            {'_id': ObjectId('6711158485d1d4c8dfd8fce4'),
             'nome': 'Cenário 1',
             'descricao': 'Cenário de venda de parques solares + 5%',
             'data': '17/10/2024 10:47:48',
             'setor': 'solar',
             'empresa': 'Parque Solar 1',
             'tipo': 'bp',
             'parte': 2},
            {'_id': ObjectId('6711158585d1d4c8dfd8fce5'),
             'nome': 'Cenário 1',
             'descricao': 'Cenário de venda de parques solares + 5%',
             'data': '17/10/2024 10:47:48',
             'setor': 'solar',
             'empresa': 'Parque Solar 1',
             'tipo': 'bp',
             'parte': 3},
            {'_id': ObjectId('6711158585d1d4c8dfd8fce6'),
             'nome': 'Cenário 1',
             'descricao': 'Cenário de venda de parques solares + 5%',
             'data': '17/10/2024 10:47:48',
             'setor': 'solar',
             'empresa': 'Parque Solar 1',
             'tipo': 'bp',
             'parte': 4}]}
