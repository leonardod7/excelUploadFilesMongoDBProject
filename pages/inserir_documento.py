from dash import dcc, html, Input, Output, State, callback
import dash_mantine_components as dmc
from model.MongoConnection import MongoEolicasConnection
from dao.MongoCRUD import MongoDBCRUD
from app import cache  # Importar o cache configurado

# 1) Acessando o banco de dados no MongoDB Atlas - Eólicas -------------------------------------------------------------

collection_eolicas_base_name: str = "SPE Energia dos Mares"


def conectar_ao_banco(collection_name: str):
    cliente = MongoEolicasConnection()
    cliente.connect_to_db()
    eolicas_crud = MongoDBCRUD(db_connection=cliente, collection_name=collection_name)
    return cliente, eolicas_crud


def upload_section_page():
    page: html.Div = html.Div(
        id="id-upload-section-page",
        className="upload-section-page",
        children=[
            # Div - 1 -------------------------------------------------------------------------------------------
            html.Div(
                className="upload-section-page-1",
                children=[
                    html.H6(children=["Escolha o Banco de Dados no Mongo DB Atlas:"]),
                    dcc.RadioItems(
                        id='id-radio-items',
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
                # Div azul
                className="upload-section-page-2",
                children=[
                    # Div rosa
                    html.Div(className="upload-section-page-2-1",
                             children=[
                                 html.H6(children=["Escolha a Coleção de Dados:"]),
                                 html.Div(id="id-div-colecoes", children=[]),
                             ]),
                    # Div preta
                    html.Div(className="upload-section-page-2-2",
                             children=[]
                             )
                ],
            ),
        ])

    return page


# 1) Callback para pegar o valor do radio items e listar as coleções que estão no banco de dados
# Callback para listar as coleções com cache
@callback(
    Output(component_id='id-div-colecoes', component_property='children'),
    Input(component_id='id-radio-items', component_property='value')
)
def listar_colecoes_eolicas(value):
    if value == 'Eólicas':
        # Verifica se as coleções já estão no cache
        colecoes = cache.get('eolicas_colecoes')

        if not colecoes:
            # Se não estiverem no cache, acessa o banco de dados
            cliente, eolicas_crud = conectar_ao_banco(collection_name="SPE Boi Gordo")

            try:
                colecoes = eolicas_crud.list_collections()
                cache.set('eolicas_colecoes', colecoes)  # Armazena no cache
            finally:
                cliente.close_connection()  # Fecha a conexão ao banco de dados

        # Cria RadioItems dinamicamente com as coleções retornadas
        radio_items = [{'label': html.Span([html.Img(style={'width': '20px', 'height': '20px', 'marginRight': '10px'},
                                                     src='/assets/img/database.png'), collection]),
                        'value': collection} for collection in colecoes]

        dc_radio: dcc.RadioItems = dcc.RadioItems(id='id-colecoes-radio',
                                                  className="custom-radio-items",
                                                  options=radio_items,
                                                  value=radio_items[0]['value'] if radio_items else None)

        return dc_radio

    elif value == 'Solar':
        return "Banco de Dados não disponível"
    else:
        return "Banco de Dados não disponível"