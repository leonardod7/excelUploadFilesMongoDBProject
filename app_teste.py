# ESSE APP SIMULA O ENVIO DE DADOS PARA O MONGO DB, REFERENTE A UM ARQUIVO PEQUENO EXCEL COM O NOME
# DE small

# 0) Importando bibliotecas --------------------------------------------------------------------------------------------
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import base64
import io
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pymongo.errors import DuplicateKeyError

# 1) Carrega as variáveis de ambiente do arquivo .env ------------------------------------------------------------------
load_dotenv()

# 2) Conexão com o MongoDB ---------------------------------------------------------------------------------------------
class MongoConnection:
    def __init__(self) -> None:
        self.__connection_string = (
            'mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority&appName={}'
        ).format(
            os.getenv("USERNAME_4"),
            os.getenv("PASSWORD_4"),
            os.getenv("MONGO_CLUSTER_URL_4"),
            os.getenv("DATABASE_NAME_4"),
            os.getenv("MONGO_APP_NAME_4")
        )
        self.__database_name = os.getenv("DATABASE_NAME_4")
        self.__client = None
        self.__db_connection = None

    def connect_to_db(self):
        try:
            self.__client = MongoClient(self.__connection_string)
            self.__db_connection = self.__client[self.__database_name]
            print("Conexão bem-sucedida ao MongoDB Eólicas!")
        except ConnectionError as e:
            print("Erro ao conectar ao MongoDB:", e)

    def get_db_connection(self):
        return self.__db_connection

    def get_db_client(self):
        return self.__client

    def close_connection(self):
        if self.__client is not None:
            self.__client.close()  # Fecha a conexão com o MongoDB
            print("Conexão com o MongoDB, Banco de Dados fechada.")

# 3) Classe CRUD para operações no MongoDB -----------------------------------------------------------------------------
# 3) Classe CRUD para operações no MongoDB -----------------------------------------------------------------------------
class MongoDBCRUD:
    """
    Classe que contém as operações CRUD para o MongoDB.
    """

    def __init__(self, db_connection: MongoConnection, collection_name: str | None) -> None:
        self.__collection_name = collection_name
        self.__db_connection = db_connection

    def get_collection(self):
        """
        Retorna a coleção especificada pelo nome.
        :return: A coleção MongoDB
        """
        return self.__db_connection.get_db_connection()[self.__collection_name]

    def insert_many(self, documents: list) -> str:
        """
        Função que insere múltiplos documentos na coleção e evita duplicidade.
        :param documents: Lista de documentos a serem inseridos.
        :return: Mensagem de sucesso ou erro.
        """
        collection = self.get_collection()

        # Inserção dos documentos, ignorando duplicatas
        try:
            collection.insert_many(documents, ordered=False)  # `ordered=False` continua após duplicatas
            print(f"{len(documents)} documentos inseridos com sucesso.")
            return "Dados inseridos com sucesso no MongoDB."
        except DuplicateKeyError as e:
            print("Erro de chave duplicada ao inserir documentos:", e)
            return "Alguns documentos já existem no MongoDB e foram ignorados."



# Inicialização do app Dash
app = dash.Dash(__name__)

# Conexão com o MongoDB (substitua pelo seu URI de conexão)
cliente = MongoConnection()
cliente.connect_to_db()
crud = MongoDBCRUD(db_connection=cliente, collection_name="Usina 1")

# Layout do app
app.layout = html.Div([
    html.H1("Upload de Arquivo Excel"),
    dcc.Upload(
        id="upload-data",
        children=html.Button("Arraste ou selecione um arquivo Excel"),
        multiple=False
    ),
    html.Div(id="output-data-upload"),
])


# Função para processar o arquivo Excel
def parse_contents(contents):
    # Decodificando o arquivo
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    # Lendo o arquivo Excel em pandas DataFrame
    try:
        df = pd.read_excel(io.BytesIO(decoded), engine='openpyxl')
        df.columns = [str(col) for col in df.columns]  # Convertendo os nomes das colunas para string
        return df
    except Exception as e:
        return f"Erro ao ler o arquivo: {str(e)}"


# Função para salvar os dados no MongoDB
def save_to_mongo(df):
    # Convertendo DataFrame para JSON e inserindo no MongoDB
    data = df.to_dict(orient='records')  # Converte para formato de dicionário
    # Ajuste para lidar com campos exclusivos para a verificação de duplicidade
    result = crud.insert_many(data)

    return result


# Callback para fazer o upload do arquivo e salvar no MongoDB
@app.callback(
    Output(component_id="output-data-upload", component_property="children"),
    [Input(component_id="upload-data", component_property="contents")]
)
def upload_file(contents):
    if contents is None:
        return "Nenhum arquivo carregado"

    # Processa o arquivo
    df = parse_contents(contents)
    print(df)
    print(type(df))
    print(df.columns)
    print(df.dtypes)

    if isinstance(df, pd.DataFrame):
        # Salva os dados no MongoDB
        result = save_to_mongo(df)
        return f"{result}"
        cliente.close_connection()
    else:
        return df  # Retorna mensagem de erro caso não seja possível processar o arquivo





if __name__ == "__main__":
    app.run_server(debug=True, port=9832)
    # connection = MongoConnection()
    # connection.connect_to_db()
    # connection.close_connection()
