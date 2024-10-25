from bson import ObjectId

# Formato que é armazenado no dcc.Store
store = {"Cen\u00e1rios": {"Cen\u00e1rio 2": [{"_id": "67111516808999e3b2900018", "nome": "Cen\u00e1rio 2", "descricao": "Cen\u00e1rio de venda de parques solares + 5%", "data": "2024-10-17 10:45:57.889000", "setor": "solar", "empresa": "Parque Solar 1", "tipo": "dre", "parte": 1}, {"_id": "67111516808999e3b2900019", "nome": "Cen\u00e1rio 2", "descricao": "Cen\u00e1rio de venda de parques solares + 5%", "data": "2024-10-17 10:45:57.928000", "setor": "solar", "empresa": "Parque Solar 1", "tipo": "dre", "parte": 2}, {"_id": "67111516808999e3b290001a", "nome": "Cen\u00e1rio 2", "descricao": "Cen\u00e1rio de venda de parques solares + 5%", "data": "2024-10-17 10:45:57.967000", "setor": "solar", "empresa": "Parque Solar 1", "tipo": "dre", "parte": 3}, {"_id": "67111516808999e3b290001b", "nome": "Cen\u00e1rio 2", "descricao": "Cen\u00e1rio de venda de parques solares + 5%", "data": "2024-10-17 10:45:58.011000", "setor": "solar", "empresa": "Parque Solar 1", "tipo": "dre", "parte": 4}], "Cen\u00e1rio 1": [{"_id": "6711153207ea80384ddb82e5", "nome": "Cen\u00e1rio 1", "descricao": "Cen\u00e1rio de venda de parques solares + 5%", "data": "2024-10-17 10:46:25.804000", "setor": "solar", "empresa": "Parque Solar 1", "tipo": "dre", "parte": 1}, {"_id": "6711153207ea80384ddb82e6", "nome": "Cen\u00e1rio 1", "descricao": "Cen\u00e1rio de venda de parques solares + 5%", "data": "2024-10-17 10:46:25.847000", "setor": "solar", "empresa": "Parque Solar 1", "tipo": "dre", "parte": 2}, {"_id": "6711153207ea80384ddb82e7", "nome": "Cen\u00e1rio 1", "descricao": "Cen\u00e1rio de venda de parques solares + 5%", "data": "2024-10-17 10:46:25.889000", "setor": "solar", "empresa": "Parque Solar 1", "tipo": "dre", "parte": 3}, {"_id": "6711153207ea80384ddb82e8", "nome": "Cen\u00e1rio 1", "descricao": "Cen\u00e1rio de venda de parques solares + 5%", "data": "2024-10-17 10:46:25.936000", "setor": "solar", "empresa": "Parque Solar 1", "tipo": "dre", "parte": 4}, {"_id": "6711158485d1d4c8dfd8fce3", "nome": "Cen\u00e1rio 1", "descricao": "Cen\u00e1rio de venda de parques solares + 5%", "data": "2024-10-17 10:47:48.514000", "setor": "solar", "empresa": "Parque Solar 1", "tipo": "bp", "parte": 1}, {"_id": "6711158485d1d4c8dfd8fce4", "nome": "Cen\u00e1rio 1", "descricao": "Cen\u00e1rio de venda de parques solares + 5%", "data": "2024-10-17 10:47:48.563000", "setor": "solar", "empresa": "Parque Solar 1", "tipo": "bp", "parte": 2}, {"_id": "6711158585d1d4c8dfd8fce5", "nome": "Cen\u00e1rio 1", "descricao": "Cen\u00e1rio de venda de parques solares + 5%", "data": "2024-10-17 10:47:48.612000", "setor": "solar", "empresa": "Parque Solar 1", "tipo": "bp", "parte": 3}, {"_id": "6711158585d1d4c8dfd8fce6", "nome": "Cen\u00e1rio 1", "descricao": "Cen\u00e1rio de venda de parques solares + 5%", "data": "2024-10-17 10:47:48.667000", "setor": "solar", "empresa": "Parque Solar 1", "tipo": "bp", "parte": 4}]}}

# Formato apresentado nos cards
data_final = {'Cenários': {'Cenário 2': [{'_id': ObjectId('67111516808999e3b2900018'), 'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:45:57.889000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 1}, {'_id': ObjectId('67111516808999e3b2900019'), 'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:45:57.928000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 2}, {'_id': ObjectId('67111516808999e3b290001a'), 'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:45:57.967000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 3}, {'_id': ObjectId('67111516808999e3b290001b'), 'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:45:58.011000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 4}], 'Cenário 1': [{'_id': ObjectId('6711153207ea80384ddb82e5'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:46:25.804000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 1}, {'_id': ObjectId('6711153207ea80384ddb82e6'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:46:25.847000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 2}, {'_id': ObjectId('6711153207ea80384ddb82e7'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:46:25.889000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 3}, {'_id': ObjectId('6711153207ea80384ddb82e8'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:46:25.936000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 4}, {'_id': ObjectId('6711158485d1d4c8dfd8fce3'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:47:48.514000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'bp', 'parte': 1}, {'_id': ObjectId('6711158485d1d4c8dfd8fce4'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:47:48.563000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'bp', 'parte': 2}, {'_id': ObjectId('6711158585d1d4c8dfd8fce5'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:47:48.612000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'bp', 'parte': 3}, {'_id': ObjectId('6711158585d1d4c8dfd8fce6'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17 10:47:48.667000', 'setor': 'solar', 'empresa': 'Parque Solar 1', 'tipo': 'bp', 'parte': 4}]}}

dict_ids = {}
for cenario, docs in data_final['Cenários'].items():
    dict_ids[cenario] = [doc['_id'] for doc in docs]

# resultado esperado do dict_ids
dict_ids_response = {
    'Cenário 2': [
        ObjectId('67111516808999e3b2900018'),
        ObjectId('67111516808999e3b2900019'),
        ObjectId('67111516808999e3b290001a'),
        ObjectId('67111516808999e3b290001b')],
    'Cenário 1': [
        ObjectId('6711153207ea80384ddb82e5'),
        ObjectId('6711153207ea80384ddb82e6'),
        ObjectId('6711153207ea80384ddb82e7'),
        ObjectId('6711153207ea80384ddb82e8'),
        ObjectId('6711158485d1d4c8dfd8fce3'),
        ObjectId('6711158485d1d4c8dfd8fce4'),
        ObjectId('6711158585d1d4c8dfd8fce5'),
        ObjectId('6711158585d1d4c8dfd8fce6')]}

nome_botao = 'Cenário 1'

# Verifica se o botão clicado es    # Temos que adicionar o nome "Cenários" ao dicionário. O formato final do documento precisa ser igual ao data_final
#     # que é o que está armazenado no dcc.Store
#     dict_ids_cenarios = {"Cenários": dict_ids}tá presente nos IDs

# Executar o app
if __name__ == "__main__":
    # Vamos deletar os ids do referentes ao nome do botão clicado
    if nome_botao in dict_ids:
        del dict_ids[nome_botao]
    print(dict_ids)
    dict_ids_cenarios = {"Cenários": dict_ids}
    print(dict_ids_cenarios)
