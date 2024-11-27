from dash import dcc, html, Input, Output, State, callback, ALL, no_update, callback_context, dash_table
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

                         # Div - 1 Banco de Dados ----------------------------------------------------------------------
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

                         # Div - 2 SPE Escolha -------------------------------------------------------------------------
                         html.Div(
                             className="home-section-page-2",
                             children=[
                                 html.H6(children=["Escolha a SPE:"],
                                         style={'fontWeight': 'bold', 'color': 'gray', 'fontFamily': 'Arial Narrow'}),
                                 dmc.Select(
                                     # label="With native scroll",
                                     id='id-dropdown-spe-home-page',
                                     # data=[{"label": spe, "value": spe} for spe in spes_names],
                                     # value=spes_names[0],
                                     data=[],
                                     withScrollArea=False,
                                     styles={"dropdown": {"maxHeight": 200, "overflowY": "auto"}},
                                     w=300,
                                     mt="xs",
                                     radius="sm",

                                 )
                             ]),

                         # Div - Cenário Escolha -----------------------------------------------------------------------
                         html.Div(
                             className="home-section-page-3",
                             children=[
                                 html.H6(children=["Escolha o Cenário:"],
                                         style={'fontWeight': 'bold', 'color': 'gray', 'fontFamily': 'Arial Narrow'}),
                                 dmc.Select(
                                     # label="With native scroll",
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
                     children=[
                         # TODO: DRE, BP e FCD.

                     ]),

        ])

    return page


# Callbacks ------------------------------------------------------------------------------------------------------------

# 1) Callback para alterar o nome das SPEs no dropdown conforme banco de dados selecionado
@callback(
    Output(component_id="id-dropdown-spe-home-page", component_property="data"),
    Output(component_id="id-dropdown-spe-home-page", component_property="value"),
    Input(component_id="id-radio-items-bancos-home-page", component_property="value")
)
def update_spe_dropdown(banco: str):
    if banco == 'Eólicas':
        cliente, eolicas_crud = conectar_ao_banco(collection_name=collection_eolicas_base_name,
                                                  database_name=banco)
        try:
            colecoes = eolicas_crud.list_collections()
        finally:
            cliente.close_connection()

        # Temos que verificar se a lista é vazia, pois podemos ter deletado todas as coleções
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

        # Temos que verificar se a lista é vazia, pois podemos ter deletado todas as coleções
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

        # Temos que verificar se a lista é vazia, pois podemos ter deletado todas as coleções
        if len(colecoes) == 0:
            valor_default = 'Sem coleções.'
            lista_valores = ['Sem coleções.']
        else:
            valor_default = colecoes[0]
            lista_valores = [{"label": spe, "value": spe} for spe in colecoes]

        return lista_valores, valor_default


# 2) Callback para alterar o nome dos cenários no dropdown conforme SPE escolhida
@callback(
    Output(component_id="id-dropdown-cenario-spe-home-page", component_property="data"),
    Output(component_id="id-dropdown-cenario-spe-home-page", component_property="value"),
    Input(component_id="id-dropdown-spe-home-page", component_property="value")
)
def update_cenario_dropdown(spe: str):
    cliente, crud = conectar_ao_banco(collection_name=spe, database_name='Eólicas')
    try:
        documentos = crud.list_documents()
        # Vamos listar todos os nomes dos cenários. Ele retorna uma lista com nomes de todos os documentos
        cenarios = [doc['nome'] for doc in documentos]
        # Precisamos pegar os nomes únicos, pois podemos ter cenários repetidos
        cenarios = list(set(cenarios))
        print(cenarios)  # debug
    finally:
        cliente.close_connection()

    # Temos que verificar se a lista é vazia, pois podemos ter deletado todas as coleções
    if len(cenarios) == 0:
        valor_default = 'Sem cenários.'
        lista_valores = ['Sem cenários.']
    else:
        valor_default = cenarios[0]
        lista_valores = [{"label": cenario, "value": cenario} for cenario in cenarios]

    return lista_valores, valor_default


# 3) Callback para apresentar os dados de cada SPE conforme escolha do banco de dados.
@callback(
    Output(component_id="id-home-section-page-dfs-0", component_property="children"),
    Input(component_id="id-radio-items-bancos-home-page", component_property="value"),
    Input(component_id="id-dropdown-spe-home-page", component_property="value"),
    Input(component_id="id-dropdown-cenario-spe-home-page", component_property="value")

)
def update_spe_dfs(banco: str, spe: str, nome_cenario: str):
    if banco == 'Eólicas':
        tipo: str = 'dre'
        chave: str = 'dre'
        conta_index: str = "Demonstração de Resultado"
        cenario_nome: str = nome_cenario
        tabela_dre = preparar_tabela_graph(collection_name=spe, banco=banco, tipo=tipo, chave=chave,
                                           conta_index=conta_index, cenario_nome=cenario_nome)

        tipo: str = 'bp'
        chave: str = 'bp'
        conta_index: str = "Balanço Patrimonial"
        cenario_nome: str = nome_cenario
        tabela_bp = preparar_tabela_graph(collection_name=spe, banco=banco, tipo=tipo, chave=chave,
                                          conta_index=conta_index, cenario_nome=cenario_nome)

        tipo: str = 'fcd'
        chave: str = 'fcd'
        conta_index: str = "Fluxo de Caixa Direto"
        cenario_nome: str = nome_cenario
        tabela_fcd = preparar_tabela_graph(collection_name=spe, banco=banco, tipo=tipo, chave=chave,
                                           conta_index=conta_index, cenario_nome=cenario_nome)

        dash_dre_format = format_data_table(tabela_dre)
        dash_bp_format = format_data_table(tabela_bp)
        dash_fcd_format = format_data_table(tabela_fcd)

        div_retorno = html.Div(
            children=[
                html.H6(f"DRE Gerencial da SPE {spe} referente ao banco de dados {banco}."),
                html.Hr(),
                dash_dre_format,
                html.Hr(),
                html.H6(f"BP Gerencial da SPE {spe} referente ao banco de dados {banco}."),
                html.Hr(),
                dash_bp_format,
                html.Hr(),
                html.H6(f"FCD Gerencial da SPE {spe} referente ao banco de dados {banco}."),
                html.Hr(),
                dash_fcd_format
            ]
        )

        return div_retorno

    elif banco == 'Solar':
        msg: html.Div = html.Div(
            children=[html.H6(f"Mostrando dados da SPE {spe} referente ao banco de dados {banco}.")])

        return msg

    elif banco == 'Hidrelétricas':
        msg: html.Div = html.Div(
            children=[html.H6(f"Mostrando dados da SPE {spe} referente ao banco de dados {banco}.")])

        return msg

    else:
        return html.Div(children=[html.H6(f"Mostrando dados da SPE {spe} referente ao banco de dados {banco}.")])
