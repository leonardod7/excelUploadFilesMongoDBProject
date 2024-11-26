from dash import dcc, html, Input, Output, State, callback, ALL, no_update, callback_context, dash_table
import dash_mantine_components as dmc
from functions.funcoes import conectar_ao_banco
from functions.funcoes_aux_table import preparar_df_formatado_para_table

# 1) Dados iniciais das coleções ---------------------------------------------------------------------------------------
# Usamos um nome base para cada coleção para que não tenhamos erro, pois precisamos passar um nome de coleção inicial
collection_eolicas_base_name: str = "SPE Ventos da Serra"
collection_solar_base_name: str = "Parque Solar 1"
collection_hidro_base_name: str = "UHE 1"


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
                                     w=450,
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


# TODO: Vamos fazer um callback para manter o estado selecionado do dropdown conforme a SPE escolhida em um dcc.Store.
# id-store-infotabela-usuario

# TODO: Vamos fazer um callback para apresentar os dados em formato de tabela conforme a SPE escolhida.


# Callbacks ------------------------------------------------------------------------------------------------------------

# 1) Callback para alterar o nome das SPEs nno dropdown conforme banco de dados selecionado
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


# 1) Callback para apresentar os dados de cada SPE conforme escolha do banco de dados.
@callback(
    Output(component_id="id-home-section-page-dfs-0", component_property="children"),
    Input(component_id="id-radio-items-bancos-home-page", component_property="value"),
    Input(component_id="id-dropdown-spe-home-page", component_property="value")
)
def update_spe_dfs(banco: str, spe: str):
    if banco == 'Eólicas':
        tabela_dre = preparar_df_formatado_para_table(
            collection_name=spe,
            banco=banco,
            tipo="dre",
            chave="dre",
            conta_index="Demonstração de Resultado"
        )
        # tabela_bp = preparar_df_formatado_para_table(
        #     collection_name=spe,
        #     banco=banco,
        #     tipo="bp",
        #     chave="bp",
        #     conta_index="Balanço Patrimonial"
        # )
        # tabela_fcd = preparar_df_formatado_para_table(
        #     collection_name=spe,
        #     banco=banco,
        #     tipo="fcd",
        #     chave="fcd",
        #     conta_index="Fluxo de Caixa Direto"
        # )
        dash_table_dre = dash_table.DataTable(data=tabela_dre.to_dict('records'), page_size=5)
        # dash_table_bp = dash_table.DataTable(data=tabela_bp.to_dict('records'), page_size=5)
        # dash_table_fcd = dash_table.DataTable(data=tabela_fcd.to_dict('records'), page_size=5)

        div_retorno = html.Div(
            children=[
                html.H6(f"Mostrando dados da SPE {spe} referente ao banco de dados {banco}."),
                dash_table_dre,
                # dash_table_bp,
                # dash_table_fcd
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





