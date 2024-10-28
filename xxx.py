from bson import ObjectId
import copy

# Formato que é armazenado no dcc.Store
Data_Store = {'Cenários': {'Cenário 1': [
    {'_id': '671fa67a779c91edfcf3de05', 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 11%', 'data': '2024-10-28 11:58:02.515000', 'setor': 'hidro', 'empresa': 'UHE 4', 'tipo': 'dre', 'parte': 1},
    {'_id': '671fa67a779c91edfcf3de06', 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 11%', 'data': '2024-10-28 11:58:02.532000', 'setor': 'hidro', 'empresa': 'UHE 4', 'tipo': 'dre', 'parte': 2},
    {'_id': '671fa67a779c91edfcf3de07', 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 11%', 'data': '2024-10-28 11:58:02.549000', 'setor': 'hidro', 'empresa': 'UHE 4', 'tipo': 'dre', 'parte': 3},
    {'_id': '671fa67a779c91edfcf3de08', 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 11%', 'data': '2024-10-28 11:58:02.567000', 'setor': 'hidro', 'empresa': 'UHE 4', 'tipo': 'dre', 'parte': 4}
]}}

# Formato apresentado nos cards
data_final = {'Cenários': {'Cenário 1': [
    {'_id': ObjectId('671fa67a779c91edfcf3de05'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 11%', 'data': '2024-10-28 11:58:02.515000', 'setor': 'hidro', 'empresa': 'UHE 4', 'tipo': 'dre', 'parte': 1},
    {'_id': ObjectId('671fa67a779c91edfcf3de06'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 11%', 'data': '2024-10-28 11:58:02.532000', 'setor': 'hidro', 'empresa': 'UHE 4', 'tipo': 'dre', 'parte': 2},
    {'_id': ObjectId('671fa67a779c91edfcf3de07'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 11%', 'data': '2024-10-28 11:58:02.549000', 'setor': 'hidro', 'empresa': 'UHE 4', 'tipo': 'dre', 'parte': 3},
    {'_id': ObjectId('671fa67a779c91edfcf3de08'), 'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 11%', 'data': '2024-10-28 11:58:02.567000', 'setor': 'hidro', 'empresa': 'UHE 4', 'tipo': 'dre', 'parte': 4}]
}}

# A única diferença é que os dados estão com o _id como ObjectId e no Data_Store estão como string

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

cenario_nome = 'Cenário 1'

# Verifica se o botão clicado es    # Temos que adicionar o nome "Cenários" ao dicionário. O formato final do documento precisa ser igual ao data_final
#     # que é o que está armazenado no dcc.Store
#     dict_ids_cenarios = {"Cenários": dict_ids}tá presente nos IDs




# Executar o app
if __name__ == "__main__":
    data_final_copy = copy.deepcopy(data_final)
    if cenario_nome in data_final_copy['Cenários']:
        del data_final_copy['Cenários'][cenario_nome]
    print(data_final_copy)


    # # Vamos deletar os ids do referentes ao nome do botão clicado
    # if nome_botao in dict_ids:
    #     del dict_ids[nome_botao]
    # print(dict_ids)
    # dict_ids_cenarios = {"Cenários": dict_ids}
    # print(dict_ids_cenarios)
