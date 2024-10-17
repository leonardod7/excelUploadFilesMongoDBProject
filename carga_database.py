# Importando bibliotecas ----------------------------------------------------------------------------------------------
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
import pandas as pd

# Importando classes de conexão, funções e CRUD ------------------------------------------------------------------------
from dao.MongoCRUD import MongoDBCRUD
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

usinas_solares = [
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

usinas_hidro = [
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

usinas_eolicas = [
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


# TODO: Colocar bancos de dados no mesmo projeto ao invés de projetos separados. Do jeito que está,
#  temos hidreletricas, Solar e olicas separados.


if __name__ == '__main__':

    # 1) Inserção de Dados  --------------------------------------------------------------------------------------------

    # Original
    # 1.1) Inserindo dados para as usinas eólicas ----------------------------------------------------------------------
    for nome in usinas_eolicas:

        setor: str = "eolicas"
        collection_name: str = nome
        eolicas_crud = MongoDBCRUD(db_connection=cliente_eolicas, collection_name=collection_name)
        cenario_name: str = "Cenário 1"

        documentos: list[dict] = criar_partes_documento(
            file_path='/Users/leonardo/Documents/PyCharm/Github/excelUploadFilesMongoDBProject/files/'
                      'SPE_1_Cenario1.xlsx',
            setor=setor,
            empresa_nome=nome,
            cenario_nome=cenario_name,
            descricao_cenario='Cenário com investimento em novos parques eólicos, variando 5%',
            sheet_name='DRE',
            demonstrativo_name='Demonstração de Resultado',
            nome_segunda_coluna='Driver'
        )

        for documento in documentos:
            unique_fields = {"empresa": nome, "nome": cenario_name}
            eolicas_crud.insert_document(document=documento, unique_fields=unique_fields)

    # 1.2) Inserindo dados para as usinas hidreletricas ----------------------------------------------------------------
    # for nome in usinas_hidro:
    #
    #     setor: str = "hidro"
    #     collection_name: str = nome
    #     hidro_crud = MongoDBCRUD(db_connection=cliente_hidro, collection_name=collection_name)
    #
    #     documentos: list[dict] = criar_partes_documento(
    #         file_path='/Users/leonardo/Documents/PyCharm/Github/excelUploadFilesMongoDBProject/files/'
    #                   'SPE_1_Cenario1.xlsx',
    #         setor=setor,
    #         empresa_nome=nome,
    #         cenario_nome='Cenário 1',
    #         descricao_cenario='Cenário com investimento em novas UHEs, variando 15%',
    #         sheet_name='DRE',
    #         demonstrativo_name='Demonstração de Resultado',
    #         nome_segunda_coluna='Driver'
    #     )
    #
    #     for documento in documentos:
    #         unique_fields = {"empresa": nome, "nome": "Cenário 1"}
    #         hidro_crud.insert_document(document=documento, unique_fields=unique_fields)

    # 1.3) Inserindo dados para as usinas solares ---------------------------------------------------------------------
    # for nome in usinas_solares:
    #
    #         setor: str = "solar"
    #         collection_name: str = nome
    #         solar_crud = MongoDBCRUD(db_connection=cliente_solar, collection_name=collection_name)
    #
    #         documentos: list[dict] = criar_partes_documento(
    #             file_path='/Users/leonardo/Documents/PyCharm/Github/excelUploadFilesMongoDBProject/files/'
    #                     'SPE_1_Cenario1.xlsx',
    #             setor=setor,
    #             empresa_nome=nome,
    #             cenario_nome='Cenário 1',
    #             descricao_cenario='Cenário com investimento em novos parques solares, variando 15%',
    #             sheet_name='DRE',
    #             demonstrativo_name='Demonstração de Resultado',
    #             nome_segunda_coluna='Driver'
    #         )
    #
    #         for documento in documentos:
    #             unique_fields = {"empresa": nome, "nome": "Cenário 1"}
    #             solar_crud.insert_document(document=documento, unique_fields=unique_fields)

    # 2) Consulta de Dados  ---------------------------------------------------------------------------------------------

    # 2.1) Consultando um documento referente a uma empresa ------------------------------------------------------------------------

    # collection_name: str = "SPE Alto da Serra"
    # filtro: dict = {"empresa": collection_name, "nome": "Cenário 1", "tipo": "dre"}
    # projecao = {"empresa": 1, "tipo": 1, "parte": 1, "_id": 0}
    #
    # eolicas_crud = MongoDBCRUD(db_connection=cliente_eolicas, collection_name=collection_name)
    #
    # response = eolicas_crud.select_many_documents(query=filtro, projection=projecao)
    # print(response)
    #
    # # 2.2) Consultando todos os documentos de uma coleção --------------------------------------------------------------
    # collection_name: str = "SPE Alto da Serra"
    # filtro: dict = {"empresa": collection_name}
    # projecao = {"empresa": 1, "tipo": 1, "parte": 1, "_id": 0}
    #
    # eolicas_crud = MongoDBCRUD(db_connection=cliente_eolicas, collection_name=collection_name)
    #
    # response = eolicas_crud.select_many_documents(query=filtro, projection=projecao)
    # print(response)




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
