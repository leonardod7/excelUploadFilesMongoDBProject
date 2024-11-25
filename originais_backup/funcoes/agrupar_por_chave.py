
import uuid


# Cenários (dados fictícios) -------------------------------------------------------------------------------------------
cenarios = [
    {"id": str(uuid.uuid4()), "cenario": "Cenário 1", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:45:57.889000", "tipo": "dre", "parte": 1},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 1", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:45:57.928000", "tipo": "dre", "parte": 2},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 1", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:45:57.967000", "tipo": "dre", "parte": 3},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 1", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:45:58.011000", "tipo": "dre", "parte": 4},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 2", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:47:48.514000", "tipo": "bp", "parte": 1},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 2", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:47:48.563000", "tipo": "bp", "parte": 2},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 2", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:47:48.612000", "tipo": "bp", "parte": 3},
    {"id": str(uuid.uuid4()), "cenario": "Cenário 2", "empresa": "Parque Solar 1", "descricao": "Cenário de venda de parques solares + 5%", "data": "2024-10-17T10:47:48.667000", "tipo": "bp", "parte": 4}
]

# Função de agrupamento por chave --------------------------------------------------------------------------------------
def agrupar_por_chave(lista: list[dict], chave: str):
    grupos = {}
    for item in lista:
        key = item[chave]
        if key not in grupos:
            grupos[key] = []
        grupos[key].append(item)
    return grupos


if __name__ == "__main__":
    agrupado = agrupar_por_chave(lista=cenarios, chave="cenario")
    cards = []
    for grupo, itens in agrupado.items():
        cards.append(itens)

    print(cards)
