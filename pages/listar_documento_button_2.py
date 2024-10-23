from datetime import datetime

from bson import ObjectId
from datetime import datetime
from dash import dcc, html, Input, Output, State, callback, ALL, no_update
from app import cache  # Importar o cache configurado
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from functions.agrupar_por_chave import agrupar_por_chave
from functions.funcoes import conectar_ao_banco, render_card, aplicar_formato_data
import dash_mantine_components as dmc
import json

# 1) Dados iniciais das coleções ---------------------------------------------------------------------------------------
collection_eolicas_base_name: str = "SPE Ventos da Serra"
collection_solar_base_name: str = "Parque Solar 1"
collection_hidro_base_name: str = "UHE 1"

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
                           # id={"type": "delete-button", "index": collection["_id"]}
                           ),
            ]),

            # Div com os cards
            html.Div([render_card(cenario=item) for item in itens], style={'display': 'flex',
                                                                           'flexDirection': 'column',
                                                                           # 'border': '1px solid gold',
                                                                           'padding': '10px',
                                                                           'marginBottom': '10px', })
        ], style={
            # 'border': '1px solid red',
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


# 3) Callback para listar apenas o nome das coleções com cache com Raio Items ------------------------------------------
@callback(
    Output(component_id='id-div-colecoes', component_property='children'),
    Input(component_id='id-radio-items-bancos', component_property='value')
)
def listar_colecoes(value):
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


# 4) Callback para buscar dados no banco de dados com base na coleção selecionada --------------------------------------
@callback(
    Output(component_id='id-consult-section-page-2-2-1', component_property='children'),
    [Input(component_id='id-radio-items-bancos', component_property='value'),  # Input para o banco de dados
     Input(component_id='id-div-colecoes', component_property='children'),  # Input para as coleções
     Input(component_id='id-colecoes-radio', component_property='value')],  # State para coleção de Eólicas
)
def mostrar_colecoes(db_name, colecoes_div, collection):

    # Debug -------------------------------------------------------------------------------------------------------
    # print(f"db_name: {db_name}")  # Debug
    # print(f"colecoes_div: {colecoes_div}")
    # print(f"collection: {collection}")  # Debug

    if collection:
        filtro: dict = {"empresa": collection}
        projecao = {"_id": 1, "nome": 1, "descricao": 1, "data": 1, "empresa": 1, "tipo": 1, "parte": 1, "setor": 1}

        # Conectar ao banco de dados e buscar documentos
        cliente, crud = conectar_ao_banco(collection_name=collection, database_name=db_name)

        try:
            response: list[dict] = crud.select_many_documents(query=filtro, projection=projecao)
            agrupado = agrupar_por_chave(lista=response, chave="nome")
            # print(agrupado)  # debug
            agrupado_formatado = aplicar_formato_data(agrupado)
            # print(lista_formatada)  # debug

            cards = gerar_lista_cards(agrupado_formatado)

            return cards  # Retorna a lista de documentos

        finally:
            cliente.close_connection()
    else:
        return "Nenhuma coleção selecionada."


# TODO: Teste ----------------------------------------------------------------------------------------------------------
# Função para serializar objetos não JSON
def json_serial(obj):
    if isinstance(obj, ObjectId):
        return str(obj)  # Converte ObjectId para string
    elif isinstance(obj, datetime):
        return obj.isoformat()  # Converte datetime para string ISO
    raise TypeError("Tipo não serializável")


@callback(
    Output(component_id='id-teste', component_property='children'),
    [Input(component_id='id-radio-items-bancos', component_property='value'),  # Input para o banco de dados
     Input(component_id='id-div-colecoes', component_property='children'),  # Input para as coleções
     Input(component_id='id-colecoes-radio', component_property='value')],  # State para coleção de Eólicas
)
def deletar_cenario(db_name, colecoes_div, collection):

    # Debug -------------------------------------------------------------------------------------------------------
    # print(f"db_name: {db_name}")  # Debug
    # print(f"colecoes_div: {colecoes_div}")
    # print(f"collection: {collection}")  # Debug

    # TODO: teste para receber uma selecao de documentos
    # Etapa 1 de teste - Vamos testar se conseguimos listar os documentos da coleção selecionada e colocá-los em uma div
    # Etapa 2 de teste - Vamos testar se conseguimos deletar um documento da coleção selecionada com base
    # no id do cenário selecionado.
    # Esse é o DESAFIO: Essa operação já será mais complexa, pois como identificaremos a qual conjunto de ids,
    # o botão de excluir pertence.

    if collection:

        # 1) Vamos listar todos os documentos presentes em collection
        filtro: dict = {"empresa": collection}
        projecao = {"_id": 1, "nome": 1, "descricao": 1, "data": 1, "empresa": 1, "tipo": 1, "parte": 1, "setor": 1}

        # 2) Conectar ao banco de dados e buscar documentos
        cliente, crud = conectar_ao_banco(collection_name=collection, database_name=db_name)

        try:
            response: list[dict] = crud.select_many_documents(query=filtro, projection=projecao)
            print(response)
            # Vamos converter para json apenas para testarmos se ele aparece na div de teste

            # Converte a lista para JSON
            json_data = json.dumps(response, default=json_serial)

            pre = html.Pre(json_data, style={'white-space': 'pre-wrap'})

            # Em cima dessa lista, iremos com base no click do botão de exclusão, deletar o documento referente ao id

        finally:
            cliente.close_connection()

    else:
        return "Nenhuma coleção selecionada."

    return pre




    # return no_update






# TODO: Vamos criar um callback para pegar o conteúdo das coleções listadas dependendo do banco de dados e armazenar em um dcc.Store
# TODO: Com base no conteúdo armazenado no dc.Store, ele alimentará a função mostrar colecoes. Teremos que alterar ela para que fique na mesma lógica que update_cards do app_div_del_10.py
# TODO: Criar um callback para excluir um conjunto de cards

# Obs.: O dcc.Store precisa receber o formato de lista de dicionários "list[dict" para que possa ser armazenado
# e recuperado. Cabe ressaltar que não serão salvos as informações da dre, bp e fcd, pois são muitas informações e
# não são necessárias para a consulta de documentos.

def update_store_cenarios():
    pass


def show_colecoes():
    pass


def delete_cards():
    pass





# TODO: Implementar a exclusão de documentos no banco de dados, igual ao arquivo app_div_del_10.py


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
