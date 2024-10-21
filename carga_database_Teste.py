# Importando bibliotecas ----------------------------------------------------------------------------------------------
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
import pandas as pd

# Importando classes de conexão, funções e CRUD ------------------------------------------------------------------------
from dao.MongoCRUD_Teste import MongoDBCRUD
from model.MongoConnection import MongoEolicasConnection, MongoSolarConnection, MongoHidroConnection
from functions.funcoes import *

# Instanciando as classes de conexão e CRUD ----------------------------------------------------------------------------
cliente_solar = MongoSolarConnection()
cliente_hidro = MongoHidroConnection()
cliente_eolicas = MongoEolicasConnection()

cliente_solar.connect_to_db()
cliente_hidro.connect_to_db()
cliente_eolicas.connect_to_db()


# Criando listas de nomes de usinas ------------------------------------------------------------------------------------

usinas_solares_2 = [
    "Parque Solar 1",
    "Parque Solar 2",
    "Parque Solar 3",
    "Parque Solar 4",
    "Parque Solar 5",
    "Parque Solar 6",
    "Parque Solar 7",
    "Parque Solar 8",
    "Parque Solar 9",
    "Parque Solar 10"
]

usinas_eolicas_2 = [
    "SPE Ventos da Serra",
    "SPE Brisa Forte",
    "SPE Energia dos Mares",
    "SPE Ventos do Horizonte",
    "SPE Brisa do Norte",
    "SPE Céu Azul",
    "SPE Força dos Ventos",
    "SPE Campo dos Ventos",
    "SPE Vento Sul",
    "SPE Ventania Forte",
    "SPE Brisa Leste",
    "SPE Horizonte Verde",
    "SPE Ventos da Costa",
    "SPE Alto da Serra",
    "SPE Ventos do Sul",
    "SPE Vento Forte",
    "SPE Brisa Pura",
    "SPE Ventos do Cerrado",
    "SPE Força do Norte",
    "SPE Ventos do Atlântico"
]

usinas_hidro_2 = [
    "UHE 1",
    "UHE 2",
    "UHE 3",
    "UHE 4",
    "UHE 5",
    "UHE 6",
    "UHE 7",
    "UHE 8",
    "UHE 9",
    "UHE 10",
    "UHE 11",
    "UHE 12",
    "UHE 13",
    "UHE 14",
    "UHE 15"
]

usinas_solares: list[str] = [
    "Parque Solar 1",
    "Parque Solar 2",
]


usinas_eolicas: list[str] = [
    "SPE Ventos da Serra",
    "SPE Brisa Forte",
    "SPE Energia dos Mares",
]

usinas_hidro: list[str] = [
    "UHE 1",
    "UHE 2",
    "UHE 3",

]


# TODO: Colocar bancos de dados no mesmo projeto ao invés de projetos separados. Do jeito que está,
#  temos hidreletricas, Solar e olicas separados.






if __name__ == '__main__':

    # 1) Inserção de Dados  --------------------------------------------------------------------------------------------

    # 1.1) Inserindo dados para as usinas solares ----------------------------------------------------------------------
    # for spe in usinas_solares:
    #
    #     # Input do usuário no front-end Interface Dash) ----------------------------------------------------------------
    #     setor: str = "solar"  # (Componente dropdown)
    #     collection_name: str = spe  # (Componente - input)
    #     solar_crud = MongoDBCRUD(db_connection=cliente_solar, collection_name=collection_name)
    #     cenario_name: str = "Cenário 1"  # (Componente - input)
    #     descricao: str = 'Cenário de venda de parques solares + 5%'  # (Componente - textarea)
    #     sheet_name: str = 'BP'  # BP, FCD, DRE (componente - dropdown)
    #     demonstrativo: str = 'Balanço Patrimonial'  # Demonstração de Resultado, Balanço Patrimonial, Fluxo de Caixa Direto (componente - dropdown)
    #     nome_segunda_coluna: str = "Driver"
    #
    #     documentos: list[dict] = criar_partes_documento(
    #         file_path='/Users/leonardo/Documents/PyCharm/Github/excelUploadFilesMongoDBProject/files/'
    #                   'SPE_1_Cenario1.xlsx',  # drag and drop do arquivo
    #         setor=setor,
    #         empresa_nome=spe,
    #         cenario_nome=cenario_name,
    #         descricao_cenario=descricao,
    #         sheet_name=sheet_name,
    #         demonstrativo_name=demonstrativo,
    #         nome_segunda_coluna=nome_segunda_coluna
    #     )
    #
    #     for documento in documentos:
    #         # unique_fields = {"empresa": spe, "nome": cenario_name}
    #         unique_fields = {"empresa": spe, "nome": cenario_name, "tipo": sheet_name}
    #         solar_crud.insert_document(document=documento, unique_fields=unique_fields)

    # 1.2) Inserindo dados para as usinas eólicas ----------------------------------------------------------------------
    # for spe in usinas_eolicas:
    #
    #     # Input do usuário no front-end Interface Dash) ----------------------------------------------------------------
    #     setor: str = "eolicas"  # (Componente dropdown)
    #     collection_name: str = spe  # (Componente - input)
    #     eolicas_crud = MongoDBCRUD(db_connection=cliente_eolicas, collection_name=collection_name)
    #     cenario_name: str = "Cenário 1"  # (Componente - input)
    #     descricao: str = 'Cenário de venda de parques solares + 8%'  # (Componente - textarea)
    #     sheet_name: str = 'DRE'  # BP, FCD, DRE (componente - dropdown)
    #     demonstrativo: str = 'Demonstração de Resultado'  # Demonstração de Resultado, Balanço Patrimonial, Fluxo de Caixa Direto (componente - dropdown)
    #     nome_segunda_coluna: str = "Driver"
    #
    #     documentos: list[dict] = criar_partes_documento(
    #         file_path='/Users/leonardo/Documents/PyCharm/Github/excelUploadFilesMongoDBProject/files/'
    #                   'SPE_1_Cenario1.xlsx',  # drag and drop do arquivo
    #         setor=setor,
    #         empresa_nome=spe,
    #         cenario_nome=cenario_name,
    #         descricao_cenario=descricao,
    #         sheet_name=sheet_name,
    #         demonstrativo_name=demonstrativo,
    #         nome_segunda_coluna=nome_segunda_coluna
    #     )
    #
    #     for documento in documentos:
    #         # unique_fields = {"empresa": spe, "nome": cenario_name}
    #         unique_fields = {"empresa": spe, "nome": cenario_name, "tipo": sheet_name}
    #         eolicas_crud.insert_document(document=documento, unique_fields=unique_fields)

    # 1.3) Inserindo dados para as usinas hidreletricas ----------------------------------------------------------------
    # for uhe in usinas_hidro:
    #
    #     # Input do usuário no front-end Interface Dash) ----------------------------------------------------------------
    #     setor: str = "hidro"
    #     collection_name: str = uhe
    #     hidro_crud = MongoDBCRUD(db_connection=cliente_hidro, collection_name=collection_name)
    #     cenario_name: str = "Cenário 1"
    #     descricao: str = 'Cenário de venda de parques solares + 8%'
    #     sheet_name: str = 'DRE'
    #     demonstrativo: str = 'Demonstração de Resultado'
    #     nome_segunda_coluna: str = "Driver"
    #
    #     documentos: list[dict] = criar_partes_documento(
    #         file_path='/Users/leonardo/Documents/PyCharm/Github/excelUploadFilesMongoDBProject/files/'
    #                   'SPE_1_Cenario1.xlsx',  # drag and drop do arquivo
    #         setor=setor,
    #         empresa_nome=uhe,
    #         cenario_nome=cenario_name,
    #         descricao_cenario=descricao,
    #         sheet_name=sheet_name,
    #         demonstrativo_name=demonstrativo,
    #         nome_segunda_coluna=nome_segunda_coluna
    #     )
    #
    #     for documento in documentos:
    #         unique_fields = {"empresa": uhe, "nome": cenario_name, "tipo": sheet_name}
    #         hidro_crud.insert_document(document=documento, unique_fields=unique_fields)




    # 2) Consulta de Dados  --------------------------------------------------------------------------------------------

    # 2.1) Consultando um documento referente a uma empresa ------------------------------------------------------------

    # collection_name: str = "Parque Solar 1"
    # tipo: str = "bp"
    # filtro: dict = {"empresa": collection_name, "nome": "Cenário 1", "tipo": tipo}
    # projecao = {"empresa": 1, "tipo": 1, "parte": 1, "_id": 0}
    #
    # solar_crud = MongoDBCRUD(db_connection=cliente_solar, collection_name=collection_name)
    #
    # response = solar_crud.select_many_documents(query=filtro, projection=projecao)
    # print(response)

    # 2.2) Consultando todos os documentos de uma coleção --------------------------------------------------------------

    collection_name: str = "Parque Solar 1"
    filtro: dict = {"empresa": collection_name}
    projecao = {"nome": 1, "descricao": 1, "data": 1, "empresa": 1, "tipo": 1, "parte": 1, "_id": 0}

    solar_crud = MongoDBCRUD(db_connection=cliente_solar, collection_name=collection_name)
    response: list[dict] = solar_crud.select_many_documents(query=filtro, projection=projecao)

    print(response)





    # 1.2) Apagando todos os dados das usinas solares ------------------------------------------------------------------
    # for nome in usinas_eolicas:
    #     collection_name: str = nome
    #     eolicas_crud = MongoDBCRUD(db_connection=cliente_eolicas, collection_name=collection_name)
    #     eolicas_crud.delete_all_documents()
    # Obs.: O comando acima apaga somente os documentos da coleção, mas não a coleção em si.Para apagar a coleção, é
    # necessário utilizar o método drop_collection() da classe MongoDBCRUD.


    # Fechando as conexões ---------------------------------------------------------------------------------------------

    cliente_solar.close_connection()
    cliente_hidro.close_connection()
    cliente_eolicas.close_connection()
