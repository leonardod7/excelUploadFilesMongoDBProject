# O OBJETIVO DESSE ARQUIVO É ENTENDERMOS COMO FUNCIONA A SEPARAÇÃO DE DOCUMENTOS E A CRIAÇÃO DE DATAFRAMES CONCATENADOS
# A PARTIR DE DOCUMENTOS MONGO. A PARTIR DESSE ARUQIVO, GEROU-SE O CÓDIGO QUE ESTÁ NO ARQUIVO "datatable_dfs.py"

# 1) Importando bibliotecas --------------------------------------------------------------------------------------------
import pandas as pd
from bson import ObjectId
from datetime import datetime

# 2) Criando funções ---------------------------------------------------------------------------------------------------
def separar_documentos(lista_documentos):
    # Inicializa as listas para os tipos
    lista_dre = []
    lista_bp = []
    lista_fcd = []

    # Itera sobre os documentos e adiciona nas listas apropriadas
    for doc in lista_documentos:
        if doc['tipo'] == 'dre':
            lista_dre.append(doc)
        elif doc['tipo'] == 'bp':
            lista_bp.append(doc)
        elif doc['tipo'] == 'fcd':
            lista_fcd.append(doc)

    # Retorna as listas
    return lista_dre, lista_bp, lista_fcd

def criar_df_concatenado(documentos, tipo, chave) -> pd.DataFrame:
    """
    Cria um DataFrame concatenado para um tipo específico de documento.

    :param documentos: Lista de documentos filtrados.
    :param tipo: Tipo de documento a ser concatenado ('dre', 'bp', 'fcd').
    :param chave: Chave no documento que contém os dados ('dre', 'bp', 'fcd').
    :return: DataFrame concatenado ou vazio caso não existam documentos.
    """
    lista_dfs: list[pd.DataFrame] = [pd.DataFrame(doc[chave]) for doc in documentos if doc['tipo'] == tipo]

    if not lista_dfs:  # Verifica se a lista está vazia
        return pd.DataFrame()  # Retorna um DataFrame vazio

    df_concatenado: pd.DataFrame = pd.concat(lista_dfs, ignore_index=True)
    return df_concatenado

# documentos que saem do mongo após a consulta de "documentos = crud.list_documents()"
documentos_mongo = [{
    '_id': ObjectId('67447a163ded1f599a580797'),
    'nome': 'Cenário 1',
    'descricao': 'Capex demanda de 2021 a 2025',
    'data': datetime(2024, 11, 25, 10, 22, 30, 433000),
    'setor': 'eolicas',
    'empresa': 'SPE Carazinho',
    'dre': [{
        'Demonstração de Resultado': 'Receita Líquida', 'Driver': '000 / Mes', 'Data': '2021-01-01', 'Valor': 1000000.0
    }],
    'tipo': 'dre',
    'parte': 1
},
    {
        '_id': ObjectId('67447a163ded1f599a580797'),
        'nome': 'Cenário 1',
        'descricao': 'Capex demanda de 2021 a 2025',
        'data': datetime(2024, 11, 25, 10, 22, 30, 433000),
        'setor': 'eolicas',
        'empresa': 'SPE Carazinho',
        'dre': [{
            'Demonstração de Resultado': 'Receita Líquida', 'Driver': '000 / Mes', 'Data': '2021-01-01', 'Valor': 2000000.0
        }],
        'tipo': 'dre',
        'parte': 2
    },
    {
        '_id': ObjectId('67447a163ded1f599a580797'),
        'nome': 'Cenário 1',
        'descricao': 'Capex demanda de 2021 a 2025',
        'data': datetime(2024, 11, 25, 10, 22, 30, 433000),
        'setor': 'eolicas',
        'empresa': 'SPE Carazinho',
        'dre': [{
            'Demonstração de Resultado': 'Receita Líquida', 'Driver': '000 / Mes', 'Data': '2021-01-01', 'Valor': 3000000.0
        }],
        'tipo': 'dre',
        'parte': 3
    },
    {
        '_id': ObjectId('67447a163ded1f599a580797'),
        'nome': 'Cenário 1',
        'descricao': 'Capex demanda de 2021 a 2025',
        'data': datetime(2024, 11, 25, 10, 22, 30, 433000),
        'setor': 'eolicas',
        'empresa': 'SPE Carazinho',
        'dre': [{
            'Demonstração de Resultado': 'Receita Líquida', 'Driver': '000 / Mes', 'Data': '2021-01-01', 'Valor': 4000000.0
        }],
        'tipo': 'dre',
        'parte': 4
    },
    {
        '_id': ObjectId('67447a163ded1f599a580797'),
        'nome': 'Cenário 1',
        'descricao': 'Capex demanda de 2021 a 2025',
        'data': datetime(2024, 11, 25, 10, 22, 30, 433000),
        'setor': 'eolicas',
        'empresa': 'SPE Carazinho',
        'bp': [{
            'Balanço Patrimonial': 'Receita Líquida', 'Driver': '000 / Mes', 'Data': '2021-01-01', 'Valor': 1000000.0
        }],
        'tipo': 'bp',
        'parte': 1
    },
    {
        '_id': ObjectId('67447a163ded1f599a580797'),
        'nome': 'Cenário 1',
        'descricao': 'Capex demanda de 2021 a 2025',
        'data': datetime(2024, 11, 25, 10, 22, 30, 433000),
        'setor': 'eolicas',
        'empresa': 'SPE Carazinho',
        'bp': [{
            'Balanço Patrimonial': 'Receita Líquida', 'Driver': '000 / Mes', 'Data': '2021-01-01', 'Valor': 1000000.0
        }],
        'tipo': 'bp',
        'parte': 2
    },
    {
        '_id': ObjectId('67447a163ded1f599a580797'),
        'nome': 'Cenário 1',
        'descricao': 'Capex demanda de 2021 a 2025',
        'data': datetime(2024, 11, 25, 10, 22, 30, 433000),
        'setor': 'eolicas',
        'empresa': 'SPE Carazinho',
        'bp': [{
            'Balanço Patrimonial': 'Receita Líquida', 'Driver': '000 / Mes', 'Data': '2021-01-01', 'Valor': 1000000.0
        }],
        'tipo': 'bp',
        'parte': 3
    },
    {
        '_id': ObjectId('67447a163ded1f599a580797'),
        'nome': 'Cenário 1',
        'descricao': 'Capex demanda de 2021 a 2025',
        'data': datetime(2024, 11, 25, 10, 22, 30, 433000),
        'setor': 'eolicas',
        'empresa': 'SPE Carazinho',
        'bp': [{
            'Balanço Patrimonial': 'Receita Líquida', 'Driver': '000 / Mes', 'Data': '2021-01-01', 'Valor': 1000000.0
        }],
        'tipo': 'bp',
        'parte': 4
    },
    # {
    #     '_id': ObjectId('67447a163ded1f599a580797'),
    #     'nome': 'Cenário 1',
    #     'descricao': 'Capex demanda de 2021 a 2025',
    #     'data': datetime(2024, 11, 25, 10, 22, 30, 433000),
    #     'setor': 'eolicas',
    #     'empresa': 'SPE Carazinho',
    #     'fcd': [{
    #         'Fluxo de Caixa': 'Receita Líquida', 'Driver': '000 / Mes', 'Data': '2021-01-01', 'Valor': 1000000.0
    #     }],
    #     'tipo': 'fcd',
    #     'parte': 1
    # },
    # {
    #     '_id': ObjectId('67447a163ded1f599a580797'),
    #     'nome': 'Cenário 1',
    #     'descricao': 'Capex demanda de 2021 a 2025',
    #     'data': datetime(2024, 11, 25, 10, 22, 30, 433000),
    #     'setor': 'eolicas',
    #     'empresa': 'SPE Carazinho',
    #     'fcd': [{
    #         'Fluxo de Caixa': 'Receita Líquida', 'Driver': '000 / Mes', 'Data': '2021-01-01', 'Valor': 1000000.0
    #     }],
    #     'tipo': 'fcd',
    #     'parte': 2
    # },
    # {
    #     '_id': ObjectId('67447a163ded1f599a580797'),
    #     'nome': 'Cenário 1',
    #     'descricao': 'Capex demanda de 2021 a 2025',
    #     'data': datetime(2024, 11, 25, 10, 22, 30, 433000),
    #     'setor': 'eolicas',
    #     'empresa': 'SPE Carazinho',
    #     'fcd': [{
    #         'Fluxo de Caixa': 'Receita Líquida', 'Driver': '000 / Mes', 'Data': '2021-01-01', 'Valor': 1000000.0
    #     }],
    #     'tipo': 'fcd',
    #     'parte': 3
    # },
    # {
    #     '_id': ObjectId('67447a163ded1f599a580797'),
    #     'nome': 'Cenário 1',
    #     'descricao': 'Capex demanda de 2021 a 2025',
    #     'data': datetime(2024, 11, 25, 10, 22, 30, 433000),
    #     'setor': 'eolicas',
    #     'empresa': 'SPE Carazinho',
    #     'fcd': [{
    #         'Fluxo de Caixa': 'Receita Líquida', 'Driver': '000 / Mes', 'Data': '2021-01-01', 'Valor': 1000000.0
    #     }],
    #     'tipo': 'fcd',
    #     'parte': 4
    # },
]


if __name__ == '__main__':
    dre, bp, fcd = separar_documentos(documentos_mongo)
    df_dre_combinado = criar_df_concatenado(documentos=dre, tipo='dre', chave='dre')
    df_bp_combinado = criar_df_concatenado(documentos=bp, tipo='bp', chave='bp')
    df_fcd_combinado = criar_df_concatenado(documentos=fcd, tipo='fcd', chave='fcd')

    print("DataFrame DRE:")
    print(df_dre_combinado)

    print("\nDataFrame BP:")
    print(df_bp_combinado)

    print("\nDataFrame FCD (vazio):")
    print(df_fcd_combinado)




