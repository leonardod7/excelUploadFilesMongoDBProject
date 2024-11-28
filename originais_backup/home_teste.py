from dash import dcc, html, Input, Output, callback
import dash_mantine_components as dmc
from functions.funcoes import conectar_ao_banco
from functions.funcoes_aux_table import preparar_tabela_graph
from functions.funcao_table import format_data_table

# 1) Dados iniciais das coleções ---------------------------------------------------------------------------------------
# Usamos um nome base para cada coleção para que não tenhamos erro, pois precisamos passar um nome de coleção inicial
collection_eolicas_base_name: str = "SPE Ventos da Serra"
collection_solar_base_name: str = "Parque Solar 1"
collection_hidro_base_name: str = "UHE 1"

# TODO: Fazer callback para manter o estado selecionado do dropdown conforme a SPE escolhida em um dcc.Store.
# TODO: Temos que pensar em como otimizar o consumo de dados no mongo db.
# TODO: Temos que atualizar o estado quando inserimos uma informação e ela retorna "Arquivo Inserido com Sucesso".

def home_page() -> html.Div:
    page: html.Div = html.Div(
        id="id-home-page",
        className="home-section-page",
        children=[
            html.Div(className="home-section-page-0",
                     children=[
                         html.Div(
                             className="home-section-page-1",
                             children=[
                                 html.H6(children=["Escolha o Banco de Dados no Mongo DB Atlas:"],
                                         style={'fontWeight': 'bold', 'color': 'gray', 'fontFamily': 'Arial Narrow'}),
                                 dcc.RadioItems(
                                     id='id-radio-items-bancos-home-page',
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

                         html.Div(
                             className="home-section-page-2",
                             children=[
                                 html.H6(children=["Escolha a SPE:"],
                                         style={'fontWeight': 'bold', 'color': 'gray', 'fontFamily': 'Arial Narrow'}),
                                 dmc.Select(
                                     id='id-dropdown-spe-home-page',
                                     data=[],
                                     withScrollArea=False,
                                     styles={"dropdown": {"maxHeight": 200, "overflowY": "auto"}},
                                     w=300,
                                     mt="xs",
                                     radius="sm",
                                 )
                             ]),

                         html.Div(
                             className="home-section-page-3",
                             children=[
                                 html.H6(children=["Escolha o Cenário:"],
                                         style={'fontWeight': 'bold', 'color': 'gray', 'fontFamily': 'Arial Narrow'}),
                                 dmc.Select(
                                     id='id-dropdown-cenario-spe-home-page',
                                     data=[],
                                     withScrollArea=False,
                                     styles={"dropdown": {"maxHeight": 200, "overflowY": "auto"}},
                                     w=300,
                                     mt="xs",
                                     radius="sm",
                                 )
                             ]),

                     ]),

            html.Div(className="home-section-page-dfs-0",
                     id="id-home-section-page-dfs-0",
                     children=[])
        ])

    return page


@callback(
    Output("id-dropdown-spe-home-page", "data"),
    Output("id-dropdown-spe-home-page", "value"),
    Input("id-radio-items-bancos-home-page", "value")
)
def update_spe_dropdown(banco: str):
    if banco == 'Eólicas':
        cliente, eolicas_crud = conectar_ao_banco(collection_name=collection_eolicas_base_name,
                                                  database_name=banco)
        try:
            colecoes = eolicas_crud.list_collections()
        finally:
            cliente.close_connection()

        if len(colecoes) == 0:
            valor_default = 'Sem coleções.'
            lista_valores = ['Sem coleções.']
        else:
            valor_default = colecoes[0]
            lista_valores = [{"label": spe, "value": spe} for spe in colecoes]

        return lista_valores, valor_default

    elif banco == 'Solar':
        cliente, solar_crud = conectar_ao_banco(collection_name=collection_solar_base_name,
                                                database_name=banco)
        try:
            colecoes = solar_crud.list_collections()
        finally:
            cliente.close_connection()

        if len(colecoes) == 0:
            valor_default = 'Sem coleções.'
            lista_valores = ['Sem coleções.']
        else:
            valor_default = colecoes[0]
            lista_valores = [{"label": spe, "value": spe} for spe in colecoes]

        return lista_valores, valor_default

    elif banco == 'Hidrelétricas':
        cliente, hidro_crud = conectar_ao_banco(collection_name=collection_hidro_base_name,
                                                database_name=banco)
        try:
            colecoes = hidro_crud.list_collections()
        finally:
            cliente.close_connection()

        if len(colecoes) == 0:
            valor_default = 'Sem coleções.'
            lista_valores = ['Sem coleções.']
        else:
            valor_default = colecoes[0]
            lista_valores = [{"label": spe, "value": spe} for spe in colecoes]

        return lista_valores, valor_default


@callback(
    Output("id-dropdown-cenario-spe-home-page", "data"),
    Output("id-dropdown-cenario-spe-home-page", "value"),
    Input("id-dropdown-spe-home-page", "value")
)
def update_cenario_dropdown(spe: str):
    cliente, crud = conectar_ao_banco(collection_name=spe, database_name='Eólicas')
    try:
        documentos = crud.list_documents()
        cenarios = [doc['nome'] for doc in documentos]
        cenarios = list(set(cenarios))
    finally:
        cliente.close_connection()

    if len(cenarios) == 0:
        valor_default = 'Sem cenários.'
        lista_valores = ['Sem cenários.']
    else:
        valor_default = cenarios[0]
        lista_valores = [{"label": cenario, "value": cenario} for cenario in cenarios]

    return lista_valores, valor_default


@callback(
    Output("id-home-section-page-dfs-0", "children"),
    Input("id-radio-items-bancos-home-page", "value"),
    Input("id-dropdown-spe-home-page", "value"),
    Input("id-dropdown-cenario-spe-home-page", "value")
)
def update_spe_dfs(banco: str, spe: str, nome_cenario: str):

    def gerar_tabela(tipo: str, chave: str, conta_index: str, cenario_nome: str):
        tabela = preparar_tabela_graph(collection_name=spe, banco=banco, tipo=tipo, chave=chave,
                                       conta_index=conta_index, cenario_nome=cenario_nome)
        return format_data_table(tabela)

    if banco == 'Eólicas':
        return html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Loading(
                            id="loading-dre",
                            type="circle",
                            fullscreen=True,
                            children=[
                                html.Div([
                                    html.H6(f"DRE Gerencial da SPE {spe} referente ao banco de dados {banco}."),
                                    gerar_tabela('dre', 'dre', "Demonstração de Resultado", nome_cenario)
                                ])
                            ]
                        )
                    ],
                    style={'marginBottom': '20px'}
                ),
                html.Div(
                    children=[
                        dcc.Loading(
                            id="loading-bp",
                            type="circle",
                            fullscreen=True,
                            children=[
                                html.Div([
                                    html.H6(f"BP Gerencial da SPE {spe} referente ao banco de dados {banco}."),
                                    gerar_tabela('bp', 'bp', "Balanço Patrimonial", nome_cenario)
                                ])
                            ]
                        )
                    ],
                    style={'marginBottom': '20px'}
                ),
                html.Div(
                    children=[
                        dcc.Loading(
                            id="loading-fcd",
                            type="circle",
                            fullscreen=True,
                            children=[
                                html.Div([
                                    html.H6(f"FCD Gerencial da SPE {spe} referente ao banco de dados {banco}."),
                                    gerar_tabela('fcd', 'fcd', "Fluxo de Caixa Direto", nome_cenario)
                                ])
                            ]
                        )
                    ],
                    style={'marginBottom': '20px'}
                )
            ]
        )

    elif banco == 'Solar':
        return html.Div(children=[
            dcc.Loading(
                id="loading-solar",
                type="circle",
                children=[
                    html.H6(f"Mostrando dados da SPE {spe} referente ao banco de dados {banco}.")
                ]
            )
        ])

    elif banco == 'Hidrelétricas':
        return html.Div(children=[
            dcc.Loading(
                id="loading-hidro",
                type="circle",
                children=[
                    html.H6(f"Mostrando dados da SPE {spe} referente ao banco de dados {banco}.")
                ]
            )
        ])

    else:
        return html.Div(children=[
            dcc.Loading(
                id="loading-default",
                type="circle",
                children=[
                    html.H6(f"Mostrando dados da SPE {spe} referente ao banco de dados {banco}.")
                ]
            )
        ])

