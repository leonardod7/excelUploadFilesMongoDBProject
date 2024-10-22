from datetime import datetime
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html

from dao.MongoCRUD import MongoDBCRUD
from model.MongoConnection import MongoEolicasConnection, MongoSolarConnection, MongoHidroConnection

# 1) Função para criar as partes do documento --------------------------------------------------------------------------
def criar_partes_documento(file_path: str, setor: str, empresa_nome: str, cenario_nome: str,
                           descricao_cenario: str, sheet_name: str, demonstrativo_name: str, nome_segunda_coluna: str) -> list[dict]:

    """
    O objetivo dessa função é transformar o demonstrativo de cada empresa em partes menores e torná-las documentos que possam ser salvos no MongoDB Atlas
    sem o risco de ultrapassar o tamanho de array recomendado pelo MongoDB.

    :param file_path: Caminho do arquivo Excel
    :param setor: Setor da empresa (eolicas, solar, hidrelétrica, etc)
    :param empresa_nome: Nome da empresa (SPE Moinhos de Vento, SPE Solar Leste, etc)
    :param cenario_nome: Nome do cenário (Cenário 1, Cenário 2, etc)
    :param descricao_cenario: Descrição do cenário (Cenário com investimento em novos parques eólicos)
    :param sheet_name: Nome da aba do arquivo Excel (DRE, FCD, BP)
    :param demonstrativo_name: Nome do demonstrativo (Demonstração de Resultado, Balanço Patrimonial, Fluxo de Caixa Direto)
    :param nome_segunda_coluna: Nome da segunda coluna do demonstrativo (Driver)
    :return: Retorna uma lista com dicionários referentes a cada parte do demonstrativo
    """

    xls = pd.ExcelFile(file_path)
    dre = pd.read_excel(xls, sheet_name=sheet_name)

    # numero_colunas = dre.shape[1]
    # print(numero_colunas)  # Mostra o número de colunas do DataFrame

    # As duas primeiras colunas
    colunas_iniciais = dre.iloc[:, :2]

    # Dividindo o DataFrame em três partes
    df_part_1 = dre.iloc[:, :50]  # As primeiras 70 colunas


    chave_name = 'dre' if sheet_name == 'DRE' else 'bp' if sheet_name == 'BP' else 'fcd'



    # Para as partes 2 e 3, concatenamos as duas primeiras colunas com as colunas específicas
    df_part_2 = pd.concat([colunas_iniciais, dre.iloc[:, 50:100]], axis=1)  # Duas primeiras + colunas 50 a 100
    df_part_3 = pd.concat([colunas_iniciais, dre.iloc[:, 100:150]], axis=1)  # Duas primeiras + colunas 100 a 150
    df_part_4 = pd.concat([colunas_iniciais, dre.iloc[:, 150:]], axis=1)  # Duas primeiras + colunas 152 em diante

    # 1) Criando o primeiro documento --------------------------------------------------------------------------------

    df_long_1 = df_part_1.melt(id_vars=[demonstrativo_name, nome_segunda_coluna], var_name='Data', value_name='Valor')
    df_list_part_1 = df_long_1.to_dict(orient='records')

    documento_spe_dre_part_1 = {
        "nome": cenario_nome,
        "descricao": descricao_cenario,
        "data": datetime.now(),
        "setor": setor,
        "empresa": empresa_nome,
        chave_name: df_list_part_1,
        "tipo": chave_name,
        "parte": 1
    }

    # 2) Criando o segundo documento ---------------------------------------------------------------------------------

    df_long_2 = df_part_2.melt(id_vars=[demonstrativo_name, nome_segunda_coluna], var_name='Data', value_name='Valor')
    df_list_part_2 = df_long_2.to_dict(orient='records')

    documento_spe_dre_part_2 = {
        "nome": cenario_nome,
        "descricao": descricao_cenario,
        "data": datetime.now(),
        "setor": setor,
        "empresa": empresa_nome,
        chave_name: df_list_part_2,
        "tipo": chave_name,
        "parte": 2
    }

    # 3) Criando o terceiro documento --------------------------------------------------------------------------------

    df_long_3 = df_part_3.melt(id_vars=[demonstrativo_name, nome_segunda_coluna], var_name='Data', value_name='Valor')
    df_list_part_3 = df_long_3.to_dict(orient='records')

    documento_spe_dre_part_3 = {
        "nome": cenario_nome,
        "descricao": descricao_cenario,
        "data": datetime.now(),
        "setor": setor,
        "empresa": empresa_nome,
        chave_name: df_list_part_3,
        "tipo": chave_name,
        "parte": 3
    }

    # 4) Criando o quarto documento ---------------------------------------------------------------------------------

    df_long_4 = df_part_4.melt(id_vars=[demonstrativo_name, nome_segunda_coluna], var_name='Data', value_name='Valor')
    df_list_part_4 = df_long_4.to_dict(orient='records')

    documento_spe_dre_part_4 = {
        "nome": cenario_nome,
        "descricao": descricao_cenario,
        "data": datetime.now(),
        "setor": setor,
        "empresa": empresa_nome,
        chave_name: df_list_part_4,
        "tipo": chave_name,
        "parte": 4
    }

    lista: list = [documento_spe_dre_part_1, documento_spe_dre_part_2, documento_spe_dre_part_3, documento_spe_dre_part_4]

    return lista

# 2) Função para conectar ao banco de dados e retornar as instâncias do cliente e do CRUD ------------------------------
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


# 3) Função de agrupamento por chave -----------------------------------------------------------------------------------
def agrupar_por_chave(lista: list[dict], chave: str):
    grupos = {}
    for item in lista:
        key = item[chave]
        if key not in grupos:
            grupos[key] = []
        grupos[key].append(item)
    return grupos

# 4) Função para renderizar cards --------------------------------------------------------------------------------------
def render_card(cenario) -> dbc.Card:
    card: dbc.Card = dbc.Card(
        dbc.CardBody([
            # TODO: Colocar o nome do cenário com uma imagem e botão dentro de uma div.
            # TODO: Incluir uma linha ao lado do nome
            # TODO: Incluir um botão de exclusão
            html.H4(children=[html.Span(children=[f"{cenario['nome']}"], style={'fontWeight': 'bold', 'color': 'gray'})],
                    className="card-title", style={'fontFamily': 'Arial Narrow',
                                                   'fontSize': '14px',
                                                   'borderBottom': '0.5px solid gray',
                                                   # 'paddingBottom': '5px',
                                                   'marginTop': '5px',}),

            # Div com o título, parte, empresa, data e tipo
            html.Div(children=[

                html.P(children=[
                    html.Span(children=["Parte: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                    f"{cenario['parte']}",
                    html.Span(children=[" |"], style={'fontStyle': 'italic', 'color': 'black'})  # Estilizando o separador
                ], className="card-text",
                    style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

                html.P(children=[
                    html.Span(children=["Empresa: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                    f"{cenario['empresa']}",
                    html.Span(children=[" |"], style={'fontStyle': 'italic', 'color': 'black'})  # Estilizando o separador
                ], className="card-text",
                    style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

                html.P(children=[
                    html.Span(children=["Data: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                    f"{cenario['data']}",
                    html.Span(children=[" |"], style={'fontStyle': 'italic', 'color': 'black'})  # Estilizando o separador
                ], className="card-text",
                    style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

                html.P(children=[
                    html.Span(children=["Tipo: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                    f"{cenario['tipo']}",
                    html.Span(children=[" |"], style={'fontStyle': 'italic', 'color': 'black'})  # Estilizando o separador
                ], className="card-text",
                    style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),
            ],
                style={'display': 'flex', 'flexDirection': 'row', 'gap': '35px'}
            ),

            # Div com a descrição
            html.Div(children=[
                # Texto da descrição
                html.Span(children=["Descrição: "],
                          style={
                              'fontWeight': 'bold',
                              'color': 'gray',
                              'fontSize': '14px',
                              'fontFamily': 'Arial Narrow',
                              'lineHeight': '20px'  # Ajuste para alinhar com a altura da imagem
                          }),

                # Descrição em si
                html.P(children=[f"{cenario['descricao']}"],
                       style={
                           'fontFamily': 'Arial Narrow',
                           'fontSize': '12px',
                           'margin': '0',  # Remover margens para alinhamento exato
                           'lineHeight': '20px'  # Mesma altura de linha que o span e a imagem
                       }),

                # Imagem ao lado do texto
                html.Img(src='/assets/img/excel_icon.png',
                         style={
                             'height': '20px',
                             'width': '20px',
                             'marginLeft': '260px',
                             'verticalAlign': 'middle'  # Garantir que a imagem alinhe ao centro
                         })
            ],
                style={
                    'display': 'flex',
                    'flexDirection': 'row',
                    'gap': '10px',  # Ajuste de espaço entre os elementos
                    # 'border': '1px solid #ccc',
                    'alignItems': 'center',  # Centralizar verticalmente
                    'padding': '5px'  # Um pouco mais de padding para garantir espaço interno
                }
            ),



            # Botão de exclusão
            # dbc.Button(children=["🗑️"], id={"type": "delete-button", "index": cenario["id"]}, n_clicks=0, color="danger")
        ]),
        style={'border': '1px solid #ccc',
               'margin': '10px',
               'marginBottom': '20px',
               'padding': '3px',
               'width': '600px',  # Largura fixa
               'height': '130px',  # Altura fixa
               'background': "linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), "
                             "url('/assets/img/eolicas.jpg')",
               'backgroundSize': 'cover',
               'backgroundPosition': 'center',
               'border-radius': '10px'
               }
    )
    return card
