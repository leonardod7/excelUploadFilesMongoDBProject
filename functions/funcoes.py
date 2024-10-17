from datetime import datetime
import pandas as pd

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