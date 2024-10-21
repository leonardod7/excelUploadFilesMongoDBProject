from dash import dcc, html, Input, Output, State, callback
from app import cache  # Importar o cache configurado
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from functions.agrupar_por_chave import agrupar_por_chave
from functions.funcoes import conectar_ao_banco

# 1) Dados iniciais das coleções ---------------------------------------------------------------------------------------

collection_eolicas_base_name: str = "SPE Ventos da Serra"
collection_solar_base_name: str = "Parque Solar 1"
collection_hidro_base_name: str = "UHE 1"


# Função para renderizar cards -----------------------------------------------------------------------------------------
def render_card(cenario) -> dbc.Card:
    card: dbc.Card = dbc.Card(
        dbc.CardBody([
            html.H4(children=[f"{cenario['nome']}"], className="card-title", style={'fontFamily': 'Arial Narrow',
                                                                                    'fontSize': '14px',
                                                                                    'borderBottom': '2px solid gray',
                                                                                    'paddingBottom': '5px',
                                                                                    'marginTop': '5px',
                                                                                    'border-radius': '5px'}),

            html.P(children=[html.Span(children=["Parte: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                             f"{cenario['parte']}"], className="card-text",
                   style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

            html.P(children=[html.Span(children=["Empresa: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                             f"{cenario['empresa']}"], className="card-text",
                   style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

            html.P(children=[html.Span(children=["Descrição: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                             f"{cenario['descricao']}"], className="card-text",
                   style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

            html.P(children=[html.Span(children=["Data: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                             f"{cenario['data']}"], className="card-text",
                   style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

            html.P(children=[html.Span(children=["Tipo: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                             f"{cenario['tipo']}"], className="card-text",
                   style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

            # Botão de exclusão
            # dbc.Button(children=["🗑️"], id={"type": "delete-button", "index": cenario["id"]}, n_clicks=0, color="danger")
        ]),
        style={'border': '1px solid #ccc',
               'margin': '10px',
               'padding': '5px',
               'width': '500px',  # Largura fixa
               'height': '300px',  # Altura fixa
               'background': "linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), "
                             "url('/assets/img/eolicas.jpg')",
               'backgroundSize': 'cover',
               'backgroundPosition': 'center',
               'border-radius': '10px'
               }
    )
    return card


# 2) Página de consultar documentos ------------------------------------------------------------------------------------
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
            agrupado = agrupar_por_chave(lista=response, chave="nome")

            cards = []

            for grupo, itens in agrupado.items():
                div: html.Div = html.Div(children=[
                    html.H5(children=[grupo], style={"textAlign": "center", "color": "gray", "marginTop": "10px"}),
                    html.Div([render_card(cenario=item) for item in itens], style={'display': 'flex',
                                                                                   'flexDirection': 'space-around',
                                                                                   'border': '1px solid gold',
                                                                                   'padding': '10px'})
                ])
                # print(grupo)  # debug Cenário 1, Cenário 2, etc
                # print(itens)  # debug Lista com os dicionários dos cenários parte 1, 2, 3, 4.
                cards.append(div)  # Título do grupo

            return cards  # Retorna a lista de documentos

        finally:
            cliente.close_connection()
    else:
        return "Nenhuma coleção selecionada."

# TODO: Implementar a exclusão de documentos no banco de dados, igual ao arquivo app_div_del_10.py
# TODO: Formatar melhor o tamanho das divs e cards, para que fiquem com o mesmo tamanho.

# Executar o app
if __name__ == "__main__":
    colecao = "SPE Ventos da Serra"
    cliente, crud = conectar_ao_banco(collection_name=colecao, database_name="Eólicas")
    # print(crud.list_collections())  # debug
    filtro: dict = {"empresa": colecao}
    projecao = {"_id": 1, "nome": 1, "descricao": 1, "data": 1, "empresa": 1, "tipo": 1, "parte": 1, "setor": 1}
    response: list[dict] = crud.select_many_documents(query=filtro, projection=projecao)
    # print(response)  # debug
    agrupado = agrupar_por_chave(lista=response, chave="nome")
    # Debug agrupado --------------------------------------------------------------------------------------------------
    print(agrupado)
    # {'Cenário 1': [
    #     {'_id': ObjectId('67164c6d22f6e78ed752c3ec'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 8%', 'data': datetime.datetime(2024, 10, 21, 9, 43, 24, 923000), 'setor': 'eolicas', 'empresa': 'SPE Ventos da Serra', 'tipo': 'dre', 'parte': 1},
    #     {'_id': ObjectId('67164c6d22f6e78ed752c3ed'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 8%', 'data': datetime.datetime(2024, 10, 21, 9, 43, 24, 939000), 'setor': 'eolicas', 'empresa': 'SPE Ventos da Serra', 'tipo': 'dre', 'parte': 2},
    #     {'_id': ObjectId('67164c6d22f6e78ed752c3ee'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 8%', 'data': datetime.datetime(2024, 10, 21, 9, 43, 24, 956000), 'setor': 'eolicas', 'empresa': 'SPE Ventos da Serra', 'tipo': 'dre', 'parte': 3},
    #     {'_id': ObjectId('67164c6d22f6e78ed752c3ef'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 8%', 'data': datetime.datetime(2024, 10, 21, 9, 43, 24, 973000), 'setor': 'eolicas', 'empresa': 'SPE Ventos da Serra', 'tipo': 'dre', 'parte': 4}]}
