import dash
from dash import dcc, html, Input, Output
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

class MongoDBCRUD:
    """
    Classe que contém as operações CRUD para o MongoDB.
    """

    def __init__(self, db_connection: MongoEolicasConnection, collection_name: str | None) -> None:
        self.__collection_name = collection_name
        self.__db_connection = db_connection

    def list_collections(self) -> list:
        """
        Função que lista todas as coleções presentes no banco de dados.
        :return: Lista com os nomes de todas as coleções no banco de dados.
        """
        db_connection = self.__db_connection.get_db_connection()
        return db_connection.list_collection_names()

    def get_collection(self):
        """
        Retorna a coleção especificada pelo nome.
        :return: A coleção MongoDB
        """
        return self.__db_connection.get_db_connection()[self.__collection_name]

    def list_documents(self) -> list:
        """
        Função que lista todos os documentos na coleção especificada,
        retornando apenas campos específicos.
        :return: Lista de documentos na coleção.
        """
        collection = self.get_collection()

        # Define a projeção para retornar apenas os campos desejados
        projection = {
            '_id': 1,
            'nome': 1,
            'descricao': 1,
            'data': 1,
            'setor': 1,
            'empresa': 1,
            'tipo': 1,
            'parte': 1
        }

        documents = list(collection.find({}, projection))
        return documents

# Inicializa a conexão com o MongoDB
mongo_conn = MongoEolicasConnection()
mongo_conn.connect_to_db()

# Inicializa o CRUD
crud = MongoDBCRUD(mongo_conn, None)

# Inicializa o aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    html.H1("App de Seleção de Banco de Dados"),

    dcc.Dropdown(
        id='db-dropdown',
        options=[
            {'label': 'Eólicas', 'value': 'eolicas'},
            {'label': 'Solar', 'value': 'solar'},
            {'label': 'Hidráulicas', 'value': 'hidraulicas'},
        ],
        placeholder="Selecione um banco de dados",
    ),

    dcc.Dropdown(
        id='collection-dropdown',
        placeholder="Selecione uma coleção",
    ),

    html.Div(id='collection-info'),
])

# Callback para atualizar as coleções com base na seleção do banco de dados
@app.callback(
    Output('collection-dropdown', 'options'),
    Input('db-dropdown', 'value'),
)
def update_collections(db_name):
    if db_name:
        # Atualiza o nome do banco de dados na classe CRUD
        crud.__init__(mongo_conn, None)  # Reinitialize with the new connection
        crud.__db_connection = mongo_conn.get_db_connection()
        collections = crud.list_collections()
        return [{'label': name, 'value': name} for name in collections]
    return []

# Callback para exibir informações da coleção selecionada
@app.callback(
    Output('collection-info', 'children'),
    Input('collection-dropdown', 'value'),
    Input('db-dropdown', 'value'),
)
def display_collection_info(collection_name, db_name):
    if collection_name and db_name:
        # Atualiza o nome da coleção na classe CRUD
        crud.__init__(mongo_conn, collection_name)  # Reinitialize with the new collection name
        documents = crud.list_documents()
        return html.Ul([html.Li(f"ID: {doc['_id']}, Nome: {doc['nome']}, Descrição: {doc['descricao']}, Data: {doc['data']}, Setor: {doc['setor']}, Empresa: {doc['empresa']}, Tipo: {doc['tipo']}, Parte: {doc['parte']}") for doc in documents])
    return "Selecione uma coleção para visualizar os dados."


# Executa o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True, port=9098)
