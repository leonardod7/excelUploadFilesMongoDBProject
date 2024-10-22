from dash import dcc, html, Input, Output, State, callback
import dash_mantine_components as dmc
from model.MongoConnection import MongoEolicasConnection, MongoSolarConnection, MongoHidroConnection
from dao.MongoCRUD import MongoDBCRUD
from app import cache  # Importar o cache configurado
from dash.exceptions import PreventUpdate

# 1) Acessando o banco de dados no MongoDB Atlas - Eólicas -------------------------------------------------------------

collection_eolicas_base_name: str = "SPE Alto da Serra"
collection_solar_base_name: str = "Parque Solar 1"
collection_hidro_base_name: str = "UHE 1"

def conectar_ao_banco(collection_name: str, database_name: str):
    if database_name == 'Eólicas':
        cliente = MongoEolicasConnection()
        cliente.connect_to_db()
        eolicas_crud = MongoDBCRUD(db_connection=cliente, collection_name=collection_name)
        return cliente, eolicas_crud
    elif database_name == 'Solar':
        cliente = MongoSolarConnection()
        cliente.connect_to_db()
        solar_crud = MongoDBCRUD(db_connection=cliente, collection_name=collection_name)
        return cliente, solar_crud
    else:
        cliente = MongoHidroConnection()
        cliente.connect_to_db()
        hidro_crud = MongoDBCRUD(db_connection=cliente, collection_name=collection_name)
        return cliente, hidro_crud


def upload_section_page():
    page: html.Div = html.Div(
        id="id-upload-section-page",
        className="consult-section-page",
        children=[
            # Div - 1 -------------------------------------------------------------------------------------------
            html.Div(
                className="consult-section-page-1",
                children=[
                    html.H6(children=["Escolha o Banco de Dados no Mongo DB Atlas:"]),
                    dcc.RadioItems(
                        id='id-radio-items-bancos',
                        className="custom-radio-items",
                        options=[
                            {
                                'label': html.Span([
                                    html.Img(src='/assets/img/db_cinza.png',
                                             style={'width': '20px', 'height': '20px', 'marginRight': '10px'}),
                                    "Eólicas"
                                ]),
                                'value': 'Eólicas'
                            },
                            {
                                'label': html.Span([
                                    html.Img(src='/assets/img/db_cinza.png',
                                             style={'width': '20px', 'height': '20px', 'marginRight': '10px'}),
                                    "Solar"
                                ]),
                                'value': 'Solar'
                            },
                            {
                                'label': html.Span([
                                    html.Img(src='/assets/img/db_cinza.png',
                                             style={'width': '20px', 'height': '20px', 'marginRight': '10px'}),
                                    "Hidrelétricas"
                                ]),
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
                                 html.H6(children=["Escolha a Coleção de Dados:"]),
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
        ])

    return page


# 1) Callback para listar as coleções com cache com Raio Items ---------------------------------------------------------
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
                                                          value=radio_items[0]['value'] if radio_items else None)

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
                                                        value=radio_items[0]['value'] if radio_items else None)

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
                                                        value=radio_items[0]['value'] if radio_items else None)

        return dc_radio_hidro


# 2) Callback para buscar dados no banco de dados com base na coleção selecionada --------------------------------------
@callback(
    Output(component_id='id-consult-section-page-2-2-1', component_property='children'),
    [Input(component_id='id-radio-items-bancos', component_property='value'),  # Input para o banco de dados
     Input(component_id='id-div-colecoes', component_property='children'),  # Input para as coleções
     Input(component_id='id-colecoes-radio', component_property='value')],  # State para coleção de Eólicas
)
def listar_colecoes(db_name, colecoes_div, collection):
    # Debug -------------------------------------------------------------------------------------------------------
    print(f"db_name: {db_name}")
    # print(f"colecoes_div: {colecoes_div}")

    print(f"collection: {collection}")

    if collection:
        filtro: dict = {"empresa": collection}
        projecao = {"_id": 1, "nome": 1, "descricao": 1, "data": 1, "empresa": 1, "tipo": 1, "parte": 1, "setor": 1}

        # Conectar ao banco de dados e buscar documentos
        cliente, crud = conectar_ao_banco(collection_name=collection, database_name=db_name)

        try:
            response: list[dict] = crud.select_many_documents(query=filtro, projection=projecao)
            # TODO: Vamos criar um formato de div para cada documento
            documentos_list = [html.Div(children=[f"Documento: {doc}"], style={
                'border': '1px solid #ccc',
                'margin': '10px',
                'padding': '10px',
                'width': '300px',
                'background': "linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), "
                              "url('/assets/img/eolicas.jpg')",
                'backgroundSize': 'cover',
                'backgroundPosition': 'center',
                'border-radius': '10px'
            }) for doc in response]

            return documentos_list  # Retorna a lista de documentos

        finally:
            cliente.close_connection()
    else:
        return "Nenhuma coleção selecionada."



