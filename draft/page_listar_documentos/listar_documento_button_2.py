from datetime import datetime

from bson import ObjectId
from datetime import datetime
from dash import dcc, html, Input, Output, State, callback, ALL, no_update
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
def gerar_lista_cards(agrupado_formatado):
    cards = []

    for grupo, itens in agrupado_formatado.items():
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
                           # id={"type": "delete-button", "index": agrupado_formatado["_id"]}
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
            print(response)

            # Vamos converter para o formato json, pois apenas assim conseguiremos armazenar no dcc.Store
            json_data = json.dumps(response, default=json_serial)
            # print('json data armazenado no dcc.Store: id-cenarios-store')  # debug
            # print(json_data)  # debug

        finally:
            cliente.close_connection()

    else:
        return "Nenhuma coleção selecionada."

    return json_data


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
def mostrar_cards_colecoes(cenarios: list[dict]):
    # 1) Vamos pegar os documentos em formato json que estão no dcc.Store e convertê-los para o formato desserializado
    # print('Dados Json Serealizados')
    # print(cenarios) # debug

    dados_originais = custom_json_decoder(cenarios)

    # print('Dados Originais')
    # print(dados_originais) # debug

    agrupado = agrupar_por_chave(lista=dados_originais, chave="nome")
    agrupado_formatado: dict[list[dict]] = aplicar_formato_data(agrupado)
    print('Agrupado Formatado')
    print(agrupado_formatado)
    cards = gerar_lista_cards(agrupado_formatado)

    return cards


# 3.4) Callback para deletar um documento do banco de dados ------------------------------------------------------------
# Vamos excluir os documentos com base nos ids que pertencem a um mesmo cenário
# @callback(Output(component_id="id-cenarios-store", component_property="data"),
#           Input(component_id=))


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

# TODO: precisamos de alguma forma criar um identificador para cada nome de chave acima. Por exemplo, temos
# 'Cenáro 1' e 'Cenário 2'. Precisamos de um identificador para cada um deles. Pode ser o próprio nome da chave mais
# um número. Por exemplo, 'Cenário 1' -> 'Cenário 1_1', 'Cenário 1_2', 'Cenário 1_3', 'Cenário 1_4'. O mesmo para
# 'Cenário 2'. Dessa forma, podemos identificar cada um dos cenários e deletar todos os documentos que pertencem a
# cada um deles. Talvez esse processo de criar um identificador seja necessário ser feito ao salvar os dados no dcc.Store
# Podemos criar no mesmo nível que a chave 'Cenário 2'por exmeplo, outra chave com um código único para cada cenário.
# A partir desse nome de chave, acessamos ela e deletamos todos os documentos que pertencem a ela. A necessidade de criar uma chave é para não corrermos
# o risco de se tivermos dois nomes iguais de cenário não excluirmos os outros. Exemplo:


agrupado_formatado: dict[list[dict]] = {
    'Cenário 2': {
        'id': '550e8400-e29b-41d4-a716-446655440000',
        'partes':
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
            ]}
}

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

    pass
