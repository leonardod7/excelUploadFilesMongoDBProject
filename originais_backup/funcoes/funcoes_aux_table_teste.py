# 0) Importanto funcoes do arquivo functions.funcoes -------------------------------------------------------------------
from functions.funcoes import conectar_ao_banco
import pandas as pd


# 1) Importando bibliotecas  -------------------------------------------------------------------------------------------
def process_consolidation_wide_view(df_concatenado: pd.DataFrame, conta_index: str):
    """
    Função que recebe um dataframe e consolida ele no formato wide
     :param df_concatenado: Documento dicionário a ser convertido
     :param conta_index: Nome completo do demonstrativo que pode ser: "Demonstração de Resultado",
     "Balanço Patrimonial" ou "Fluxo de Caixa Direto"
     :return: DataFrame com os dados do documento
    """

    df = df_concatenado
    conta_index: str = conta_index

    # 1) Capturar a ordem original das colunas 'Conta' e 'Driver'
    ordem_original = df[[conta_index, 'Driver']].drop_duplicates()

    # 2) Pivotar o DataFrame
    df_pivot = df.pivot_table(index=[conta_index, 'Driver'], columns='Data', values='Valor').reset_index()

    # 3) Renomear as colunas para que fiquem mais claras
    df_pivot.columns.name = None  # Remove o nome das colunas
    df_pivot = df_pivot.rename_axis(None, axis=1)  # Remove o nome do índice das colunas

    # 4) Reordenar o DataFrame de acordo com a ordem original
    df_pivot = pd.merge(ordem_original, df_pivot, on=[conta_index, 'Driver'], how='left')

    return df_pivot


def format_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Formata os títulos das colunas que representam datas para o formato brasileiro (dd/mm/yyyy),
    a partir da terceira coluna do DataFrame.

    Parâmetros:
    :param df: DataFrame original com as colunas de datas a partir da terceira.
    :return: DataFrame com os títulos das colunas de datas formatados no padrão brasileiro.
    """
    # Criar um dicionário de mapeamento para renomear as colunas a partir da terceira
    new_columns = {col: pd.to_datetime(col).strftime('%d/%m/%Y') for col in df.columns[2:]}

    # Renomear as colunas
    df = df.rename(columns=new_columns)

    return df


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

def preparar_df_formatado_para_table(collection_name: str, banco: str, tipo: str, chave: str, conta_index: str):

    cliente, crud = conectar_ao_banco(collection_name=collection_name, database_name=banco)

    try:
        documentos = crud.list_documents()
        dre, bp, fcd = separar_documentos(documentos)
        df_combinado = criar_df_concatenado(documentos=dre, tipo=tipo, chave=chave)
        wide_view = process_consolidation_wide_view(df_concatenado=df_combinado, conta_index=conta_index)
        wide_view_data_format = format_column(df=wide_view)
        return wide_view_data_format

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    finally:
        cliente.close_connection()

def filtrar_por_cenario(lista, cenario):
    return [doc for doc in lista if doc['nome'] == cenario]

def separar_e_filtrar_por_cenario(lista_documentos, cenario):

    # Separa os documentos por tipo
    lista_dre, lista_bp, lista_fcd = separar_documentos(lista_documentos)

    # Filtra cada lista pelo nome do cenário
    lista_dre_filtrada = filtrar_por_cenario(lista_dre, cenario)
    lista_bp_filtrada = filtrar_por_cenario(lista_bp, cenario)
    lista_fcd_filtrada = filtrar_por_cenario(lista_fcd, cenario)

    # Retorna as listas filtradas em um dicionário
    return {
        'dre': lista_dre_filtrada,
        'bp': lista_bp_filtrada,
        'fcd': lista_fcd_filtrada
    }

def preparar_tabela_graph(collection_name: str, banco: str, tipo: str, chave: str,
                          conta_index: str, cenario_nome: str) -> pd.DataFrame:

    cliente, crud = conectar_ao_banco(collection_name=collection_name, database_name=banco)

    try:
        documentos = crud.list_documents()
        resultado = separar_e_filtrar_por_cenario(lista_documentos=documentos, cenario=cenario_nome)
        df = resultado[tipo]
        df_combinado = criar_df_concatenado(documentos=df, tipo=tipo, chave=chave)
        wide_view = process_consolidation_wide_view(df_concatenado=df_combinado, conta_index=conta_index)
        wide_view_data_format = format_column(df=wide_view)
        return wide_view_data_format

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    finally:
        cliente.close_connection()


# 2) Criando a função --------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    collection_name: str = "SPE Carazinho"
    banco: str = "Eólicas"
    cliente, crud = conectar_ao_banco(collection_name=collection_name, database_name=banco)

    df = preparar_tabela_graph(collection_name="SPE Carazinho", banco="Eólicas", tipo="fcd", chave="fcd",
                               conta_index="Fluxo de Caixa Direto", cenario_nome="Cenário 2")
    print(df)

    # Essa forma é a forma manual de fazer sem usar a função preparar_tabela_graph
    # try:
    #     documentos = crud.list_documents()
    #     # Filtrar documentos pelo nome: 'Cenário 1'
    #     resultado: dict = separar_e_filtrar_por_cenario(documentos, 'Cenário 2')
    #     # Devemos esperar 3 documentos: 'dre', 'bp' e 'fcd'
    #     print(len(resultado))
    #     # Vamos filtrar somente a dre pelo nome da chave. Devemos esperar 4 documentos, pois ele foi dividido em 4 partes
    #     dre = resultado['dre']
    #     print(len(dre))
    #     tipo: str = 'dre'
    #     chave: str = 'dre'
    #     conta_index: str = "Demonstração de Resultado"
    #     df_combinado = criar_df_concatenado(documentos=dre, tipo=tipo, chave=chave)
    #     # print(df_combinado)
    #     wide_view = process_consolidation_wide_view(df_concatenado=df_combinado, conta_index=conta_index)
    #     wide_view_data_format = format_column(df=wide_view)
    #     print(wide_view_data_format)
    # except Exception as e:
    #     print(f"Ocorreu um erro: {e}")
    # finally:
    #     cliente.close_connection()