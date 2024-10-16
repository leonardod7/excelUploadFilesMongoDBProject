from model.MongoConnection import MongoEolicasConnection

# Carrega as variáveis de ambiente do arquivo .env


class MongoDBCRUD:

    """
    Classe que contém as operações CRUD para o MongoDB.
    """

    def __init__(self, db_connection: MongoEolicasConnection, collection_name: str | None) -> None:
        self.__collection_name = collection_name
        self.__db_connection = db_connection

    def create_collection(self, collection_name: str) -> None:
        """
        Função que cria uma nova coleção no banco de dados.
        Se uma coleção com o mesmo nome já existir, uma mensagem é exibida.
        :param collection_name: Nome da coleção a ser criada
        """
        db_connection = self.__db_connection.get_db_connection()

        # Verifica se a coleção já existe
        if collection_name in db_connection.list_collection_names():
            print(f"Já existe uma coleção com o nome '{collection_name}'.")
        else:
            db_connection.create_collection(collection_name)
            print(f"Coleção '{collection_name}' criada com sucesso.")

    def get_collection(self):
        """
        Retorna a coleção especificada pelo nome.
        :return: A coleção MongoDB
        """
        return self.__db_connection.get_db_connection()[self.__collection_name]

    def list_collections(self) -> list:
        """
        Função que lista todas as coleções presentes no banco de dados.
        :return: Lista com os nomes de todas as coleções no banco de dados.
        """
        db_connection = self.__db_connection.get_db_connection()
        return db_connection.list_collection_names()

    def insert_document(self, document: dict, unique_fields: dict = None) -> dict:
        """
        Função que insere um documento na coleção, verificando antes se ele já existe com base em 'empresa', 'nome' e 'parte'.
        :param document: Documento que queremos inserir.
        :param unique_fields: Dicionário contendo os campos 'empresa', 'nome' e outros pelos quais queremos verificar duplicidade.
        :return: Documento inserido ou o documento existente caso já tenha sido inserido anteriormente.
        """
        collection = self.get_collection()

        # Verifica se o documento contém o campo 'parte' e combina com os campos únicos
        if "parte" in document and unique_fields:
            query = {
                "empresa": unique_fields.get("empresa"),
                "nome": unique_fields.get("nome"),
                "parte": document["parte"]  # Verifica a combinação de empresa, nome e parte
            }

            # Verifica se um documento com essa combinação já existe
            existing_document = collection.find_one(query)

            if existing_document:
                print(f"Documento com empresa '{query['empresa']}', nome '{query['nome']}' e parte '{query['parte']}' já existe.")
                return existing_document  # Retorna o documento existente

        # Se não existe, insere o novo documento
        collection.insert_one(document)
        print(f"Documento com parte {document['parte']} inserido com sucesso.")

        return document

    def delete_all_documents(self):
        """
        Função que apaga todos os documentos da coleção especificada.
        """
        collection = self.get_collection()
        result = collection.delete_many({})
        print(f"{result.deleted_count} documentos foram deletados.")

    def list_documents(self) -> list:

        """
        Função que lista todos os documentos na coleção especificada.
        :return: Lista de documentos na coleção.
        """

        collection = self.get_collection()
        documents = list(collection.find())

        return documents

    def select_many_documents(self, query: dict, projection: dict = None) -> list[dict]:

        """
        Função que seleciona vários documentos da coleção com base em um filtro e uma projeção.
        :param query: Filtro de seleção, campos que queremos que sejam retornados
        :param projection: Campos que queremos que sejam retornados através de um dicionário com valores 0 ou 1, onde 0 é para excluir o campo e 1 para incluir.
        :return: Lista de documentos que atendem ao filtro passado como parâmetro
        """

        collection = self.get_collection()

        # O campo projection serve para passarmos o parâmetro dos campos que queremos que seja retornado
        data = collection.find(query, projection=projection)

        response = []

        for elemento in data:
            response.append(elemento)

        return response

    def delete_one_document(self, query: dict) -> None:
        """
        Função que apaga um documento da coleção com base em um filtro.
        :param query: Filtro para a exclusão do documento.
        """
        collection = self.get_collection()
        data = collection.delete_one(query)

        response: str = f"{data.deleted_count} documento foi deletado."

        return response


# Testando a conexão como o Mongo DB Atlas -----------------------------------------------------------------------------
if __name__ == '__main__':

    cliente = MongoEolicasConnection()
    cliente.connect_to_db()
    db_connection = cliente.get_db_connection()

    collection_name: str = "SPE Boi Gordo"
    eolicas_crud = MongoDBCRUD(db_connection=cliente, collection_name = collection_name)

    print("Coleções no banco de dados:")
    print(eolicas_crud.list_collections())

    # Fechando a conexão
    cliente.close_connection()

