from bson import ObjectId
from datetime import datetime
import json

# Função para desserializar dados
def json_deserial(data):
    # Verifica se 'data' é uma lista de documentos
    if isinstance(data, list):
        for doc in data:
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

# Função para serializar objetos não JSON
def json_serial(obj):
    if isinstance(obj, ObjectId):
        return str(obj)  # Converte ObjectId para string
    elif isinstance(obj, datetime):
        return obj.isoformat()  # Converte datetime para string ISO
    raise TypeError("Tipo não serializável")


def custom_json_decoder(json_str):
    data = json.loads(json_str)
    for item in data:
        item['_id'] = ObjectId(item['_id'])  # Convertendo o _id
        item['data'] = datetime.fromisoformat(item['data'])  # Convertendo a data
    return data


# Dados armazenados no dcc.Store
dados_serializados = [{"_id": "67111516808999e3b2900018",
                       "nome": "Cen\u00e1rio 2",
                       "descricao": "Cen\u00e1rio de venda de parques solares + 5%",
                       "data": "2024-10-17T10:45:57.889000",
                       "setor": "solar",
                       "empresa": "Parque Solar 1",
                       "tipo": "dre",
                       "parte": 1},
                      {"_id": "67111516808999e3b2900019",
                       "nome": "Cen\u00e1rio 2",
                       "descricao": "Cen\u00e1rio de venda de parques solares + 5%",
                       "data": "2024-10-17T10:45:57.928000",
                       "setor": "solar",
                       "empresa": "Parque Solar 1",
                       "tipo": "dre",
                       "parte": 2},
                      {"_id": "67111516808999e3b290001a",
                       "nome": "Cen\u00e1rio 2",
                       "descricao": "Cen\u00e1rio de venda de parques solares + 5%",
                       "data": "2024-10-17T10:45:57.967000",
                       "setor": "solar",
                       "empresa": "Parque Solar 1",
                       "tipo": "dre",
                       "parte": 3},
                      {"_id": "67111516808999e3b290001b",
                       "nome": "Cen\u00e1rio 2",
                       "descricao": "Cen\u00e1rio de venda de parques solares + 5%",
                       "data": "2024-10-17T10:45:58.011000",
                       "setor": "solar",
                       "empresa": "Parque Solar 1",
                       "tipo": "dre",
                       "parte": 4},
                      {"_id": "6711153207ea80384ddb82e5",
                       "nome": "Cen\u00e1rio 1",
                       "descricao": "Cen\u00e1rio de venda de parques solares + 5%",
                       "data": "2024-10-17T10:46:25.804000",
                       "setor": "solar",
                       "empresa": "Parque Solar 1",
                       "tipo": "dre",
                       "parte": 1},
                      {"_id": "6711153207ea80384ddb82e6",
                       "nome": "Cen\u00e1rio 1",
                       "descricao": "Cen\u00e1rio de venda de parques solares + 5%",
                       "data": "2024-10-17T10:46:25.847000",
                       "setor": "solar",
                       "empresa": "Parque Solar 1",
                       "tipo": "dre",
                       "parte": 2},
                      {"_id": "6711153207ea80384ddb82e7",
                       "nome": "Cen\u00e1rio 1",
                       "descricao": "Cen\u00e1rio de venda de parques solares + 5%",
                       "data": "2024-10-17T10:46:25.889000",
                       "setor": "solar",
                       "empresa": "Parque Solar 1",
                       "tipo": "dre",
                       "parte": 3},
                      {"_id": "6711153207ea80384ddb82e8",
                       "nome": "Cen\u00e1rio 1",
                       "descricao": "Cen\u00e1rio de venda de parques solares + 5%",
                       "data": "2024-10-17T10:46:25.936000",
                       "setor": "solar",
                       "empresa": "Parque Solar 1",
                       "tipo": "dre",
                       "parte": 4},
                      {"_id": "6711158485d1d4c8dfd8fce3",
                       "nome": "Cen\u00e1rio 1",
                       "descricao": "Cen\u00e1rio de venda de parques solares + 5%",
                       "data": "2024-10-17T10:47:48.514000",
                       "setor": "solar",
                       "empresa": "Parque Solar 1",
                       "tipo": "bp",
                       "parte": 1},
                      {"_id": "6711158485d1d4c8dfd8fce4",
                       "nome": "Cen\u00e1rio 1",
                       "descricao": "Cen\u00e1rio de venda de parques solares + 5%",
                       "data": "2024-10-17T10:47:48.563000",
                       "setor": "solar",
                       "empresa": "Parque Solar 1",
                       "tipo": "bp",
                       "parte": 2},
                      {"_id": "6711158585d1d4c8dfd8fce5",
                       "nome": "Cen\u00e1rio 1",
                       "descricao": "Cen\u00e1rio de venda de parques solares + 5%",
                       "data": "2024-10-17T10:47:48.612000",
                       "setor": "solar",
                       "empresa": "Parque Solar 1",
                       "tipo": "bp",
                       "parte": 3},
                      {"_id": "6711158585d1d4c8dfd8fce6",
                       "nome": "Cen\u00e1rio 1",
                       "descricao": "Cen\u00e1rio de venda de parques solares + 5%",
                       "data": "2024-10-17T10:47:48.667000",
                       "setor": "solar",
                       "empresa": "Parque Solar 1",
                       "tipo": "bp",
                       "parte": 4}]




dados_nao_serealizados = [{'_id': ObjectId('67164c6d22f6e78ed752c3ec'),
                           'nome': 'Cenário 1',
                           'descricao': 'Cenário de venda de parques solares + 8%',
                           'data': datetime(2024, 10, 21, 9, 43, 24, 923000),
                           'setor': 'eolicas',
                           'empresa': 'SPE Ventos da Serra',
                           'tipo': 'dre', 'parte': 1},
                          {'_id': ObjectId('67164c6d22f6e78ed752c3ed'),
                           'nome': 'Cenário 1',
                           'descricao': 'Cenário de venda de parques solares + 8%',
                           'data': datetime(2024, 10, 21, 9, 43, 24, 939000),
                           'setor': 'eolicas',
                           'empresa': 'SPE Ventos da Serra',
                           'tipo': 'dre',
                           'parte': 2}]


if __name__ == '__main__':

    # Vamos desfazer o formato json_serial para o formato original
    dados_originais = json_deserial(dados_serializados)

    # Agora, os dados estão de volta ao formato original com ObjectId e datetime
    print(dados_originais)

    # # Serializando os dados
    # dados_serealizados = json_serial(dados_nao_serealizados)
    # print(dados_serealizados)

