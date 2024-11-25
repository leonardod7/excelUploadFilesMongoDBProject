from datetime import datetime
from bson import ObjectId
import json
from functions.funcoes import agrupar_por_chave

def criar_cenarios(dicionario: dict[list[dict]]) -> dict[dict:list[dict]]:
    # Criar um novo dicionário com a chave "Cenários"
    cenarios = {"Cenários": dicionario}
    return cenarios

def json_deserial(data):
    # Verifica se 'data' é um dicionário que contém cenários
    if isinstance(data, dict) and 'Cenários' in data:
        for cenario, documentos in data['Cenários'].items():
            # Verifica se 'documentos' é uma lista
            if isinstance(documentos, list):
                for doc in documentos:
                    for key, value in doc.items():
                        # Converte strings que representam ObjectId de volta ao formato ObjectId
                        if key == '_id' and isinstance(value, str):
                            doc[key] = ObjectId(value)
                        # Converte strings ISO de volta para datetime
                        elif isinstance(value, str) and 'T' in value and ':' in value:
                            try:
                                doc[key] = datetime.fromisoformat(value)
                            except ValueError:
                                pass  # Ignora erros de conversão
    return data

# 1) Upload data from Mongo DB to dcc.Store (Step by Step) -------------------------------------------------------------

# 1.1) através da consulta retornada do banco (dados não serealizados), precisamos agrupar os dados por nome
response: list[dict] = [
    {'_id': ObjectId('67111516808999e3b2900018'),
     'nome': 'Cenário 2',
     'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime(2024, 10, 17, 10, 45, 57, 889000),
     'setor': 'solar',
     'empresa': 'Parque Solar 1',
     'tipo': 'dre',
     'parte': 1},
    {'_id': ObjectId('67111516808999e3b2900019'),
     'nome': 'Cenário 2',
     'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime(2024, 10, 17, 10, 45, 57, 928000),
     'setor': 'solar',
     'empresa': 'Parque Solar 1',
     'tipo': 'dre',
     'parte': 2},
    {'_id': ObjectId('67111516808999e3b290001a'),
     'nome': 'Cenário 2',
     'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime(2024, 10, 17, 10, 45, 57, 967000),
     'setor': 'solar',
     'empresa': 'Parque Solar 1',
     'tipo': 'dre',
     'parte': 3},
    {'_id': ObjectId('67111516808999e3b290001b'),
     'nome': 'Cenário 2',
     'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime(2024, 10, 17, 10, 45, 58, 11000),
     'setor': 'solar',
     'empresa': 'Parque Solar 1',
     'tipo': 'dre',
     'parte': 4},
    {'_id': ObjectId('6711153207ea80384ddb82e5'),
     'nome': 'Cenário 1',
     'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime(2024, 10, 17, 10, 46, 25, 804000),
     'setor': 'solar',
     'empresa': 'Parque Solar 1',
     'tipo': 'dre',
     'parte': 1},
    {'_id': ObjectId('6711153207ea80384ddb82e6'),
     'nome': 'Cenário 1',
     'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime(2024, 10, 17, 10, 46, 25, 847000),
     'setor': 'solar',
     'empresa': 'Parque Solar 1',
     'tipo': 'dre',
     'parte': 2},
    {'_id': ObjectId('6711153207ea80384ddb82e7'),
     'nome': 'Cenário 1',
     'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime(2024, 10, 17, 10, 46, 25, 889000),
     'setor': 'solar',
     'empresa': 'Parque Solar 1',
     'tipo': 'dre',
     'parte': 3},
    {'_id': ObjectId('6711153207ea80384ddb82e8'),
     'nome': 'Cenário 1',
     'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime(2024, 10, 17, 10, 46, 25, 936000),
     'setor': 'solar',
     'empresa': 'Parque Solar 1',
     'tipo': 'dre',
     'parte': 4},
    {'_id': ObjectId('6711158485d1d4c8dfd8fce3'),
     'nome': 'Cenário 1',
     'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime(2024, 10, 17, 10, 47, 48, 514000),
     'setor': 'solar',
     'empresa': 'Parque Solar 1',
     'tipo': 'bp',
     'parte': 1},
    {'_id': ObjectId('6711158485d1d4c8dfd8fce4'),
     'nome': 'Cenário 1',
     'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime(2024, 10, 17, 10, 47, 48, 563000),
     'setor': 'solar',
     'empresa': 'Parque Solar 1',
     'tipo': 'bp',
     'parte': 2},
    {'_id': ObjectId('6711158585d1d4c8dfd8fce5'),
     'nome': 'Cenário 1',
     'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime(2024, 10, 17, 10, 47, 48, 612000),
     'setor': 'solar',
     'empresa': 'Parque Solar 1',
     'tipo': 'bp',
     'parte': 3},
    {'_id': ObjectId('6711158585d1d4c8dfd8fce6'),
     'nome': 'Cenário 1',
     'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime(2024, 10, 17, 10, 47, 48, 667000),
     'setor': 'solar',
     'empresa': 'Parque Solar 1',
     'tipo': 'bp',
     'parte': 4}
]

# 1.2) Agrupando lista de dicionarios por nome
agrupado = agrupar_por_chave(lista=response, chave="nome")

# print da resposta acima
agrupado_response: dict[list[dict]] = {
    'Cenário 2': [
        {'_id': ObjectId('67111516808999e3b2900018'), 'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime(2024, 10, 17, 10, 45, 57, 889000), 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 1},
        {'_id': ObjectId('67111516808999e3b2900019'), 'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime(2024, 10, 17, 10, 45, 57, 928000), 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 2},
        {'_id': ObjectId('67111516808999e3b290001a'), 'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime(2024, 10, 17, 10, 45, 57, 967000), 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 3},
        {'_id': ObjectId('67111516808999e3b290001b'), 'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime(2024, 10, 17, 10, 45, 58, 11000), 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 4}
    ],
    'Cenário 1': [
        {'_id': ObjectId('6711153207ea80384ddb82e5'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime(2024, 10, 17, 10, 46, 25, 804000), 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 1},
        {'_id': ObjectId('6711153207ea80384ddb82e6'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime(2024, 10, 17, 10, 46, 25, 847000), 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 2},
        {'_id': ObjectId('6711153207ea80384ddb82e7'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime(2024, 10, 17, 10, 46, 25, 889000), 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 3},
        {'_id': ObjectId('6711153207ea80384ddb82e8'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime(2024, 10, 17, 10, 46, 25, 936000), 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 4}
    ],
    'Cenário 1': [
        {'_id': ObjectId('6711158485d1d4c8dfd8fce3'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime(2024, 10, 17, 10, 47, 48, 514000), 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'bp', 'parte': 1},
        {'_id': ObjectId('6711158485d1d4c8dfd8fce4'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime(2024, 10, 17, 10, 47, 48, 563000), 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'bp', 'parte': 2},
        {'_id': ObjectId('6711158585d1d4c8dfd8fce5'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime(2024, 10, 17, 10, 47, 48, 612000), 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'bp', 'parte': 3},
        {'_id': ObjectId('6711158585d1d4c8dfd8fce6'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime(2024, 10, 17, 10, 47, 48, 667000), 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'bp', 'parte': 4}
    ]
}

# 1.3) Cria dicionário para ser utilizado na estrutura do dcc.Store
cenarios: dict[dict:list[dict]] = criar_cenarios(agrupado)

# print da resposta acima
print(cenarios)  # Exibe o dicionário formatado como {'Cenários': ...}

# 1.4) Converte dicionário em JSON para ser armazenado em um dcc.Store
json_cenarios = json.dumps(cenarios, default=str) # Dados que serão armazenados no dcc.Store
print(json_cenarios)  # Exibe o JSON gerado

# 1.5) Agora, precisamos deserializar o JSON de volta para o dicionário com os tipos corretos
data_deserializada = json.loads(json_cenarios)
data_final: dict[dict:list[dict]] = json_deserial(data_deserializada)  # Dados que serão utilizados

print(data_final)  # Exibe o dicionário deserializado
