from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


class MongoEolicasConnection:
    def __init__(self) -> None:
        self.__connection_string = (
            'mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority&appName={}'
        ).format(
            os.getenv("USERNAME"),
            os.getenv("PASSWORD"),
            os.getenv("MONGO_CLUSTER_URL"),
            os.getenv("DATABASE_NAME"),
            os.getenv("MONGO_APP_NAME")
        )
        self.__database_name = os.getenv("DATABASE_NAME")
        self.__client = None
        self.__db_connection = None

    def connect_to_db(self):
        try:
            self.__client = MongoClient(self.__connection_string)
            self.__db_connection = self.__client[self.__database_name]
            print("Conexão bem-sucedida ao MongoDB!")
        except ConnectionError as e:
            print("Erro ao conectar ao MongoDB:", e)

    def get_db_connection(self):
        return self.__db_connection

    def get_db_client(self):
        return self.__client

    def close_connection(self):
        if self.__client is not None:
            self.__client.close()  # Fecha a conexão com o MongoDB
            print("Conexão com o MongoDB fechada.")


# Testando a Conexão com o MongoDB Atlas -------------------------------------------------------------------------------
if __name__ == '__main__':
    connection = MongoEolicasConnection()
    connection.connect_to_db()
    connection.close_connection()
