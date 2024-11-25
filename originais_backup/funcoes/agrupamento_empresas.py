from collections import defaultdict
from pprint import pprint
import datetime


# Função para agrupar os dicionários
def agrupar_por_chaves(lista_dicionarios: list[dict]) -> list[list[dict]]:

    """
    Função para agrupar os dicionários com base nas chaves 'nome', 'descricao', 'empresa' e 'tipo'
    :param lista_dicionarios: recebe uma lista de dicionários
    :return: retorna uma lista de listas de dicionários
    """

    grupos = defaultdict(list)  # Dicionário para agrupar

    # Agrupando com base nas chaves 'nome', 'descricao', 'empresa' e 'tipo'
    for dicionario in lista_dicionarios:
        chave = (dicionario['nome'], dicionario['descricao'], dicionario['empresa'], dicionario['tipo'])
        grupos[chave].append(dicionario)

    # Convertendo para lista de listas
    lista_agrupada = list(grupos.values())

    return lista_agrupada


if __name__ == '__main__':

    lista_dict_2: list[dict] = [
        {'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime.datetime(2024, 10, 17, 10, 45, 57, 889000), 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 1},
        {'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime.datetime(2024, 10, 17, 10, 45, 57, 928000), 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 2},
        {'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime.datetime(2024, 10, 17, 10, 45, 57, 967000), 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 3},
        {'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime.datetime(2024, 10, 17, 10, 45, 58, 11000), 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 4},
        {'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime.datetime(2024, 10, 17, 10, 46, 25, 804000), 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 1},
        {'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime.datetime(2024, 10, 17, 10, 46, 25, 847000), 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 2},
        {'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime.datetime(2024, 10, 17, 10, 46, 25, 889000), 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 3},
        {'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime.datetime(2024, 10, 17, 10, 46, 25, 936000), 'empresa': 'Parque Solar 1', 'tipo': 'dre', 'parte': 4},
        {'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime.datetime(2024, 10, 17, 10, 47, 48, 514000), 'empresa': 'Parque Solar 1', 'tipo': 'bp', 'parte': 1},
        {'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime.datetime(2024, 10, 17, 10, 47, 48, 563000), 'empresa': 'Parque Solar 1', 'tipo': 'bp', 'parte': 2},
        {'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime.datetime(2024, 10, 17, 10, 47, 48, 612000), 'empresa': 'Parque Solar 1', 'tipo': 'bp', 'parte': 3},
        {'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': datetime.datetime(2024, 10, 17, 10, 47, 48, 667000), 'empresa': 'Parque Solar 1', 'tipo': 'bp', 'parte': 4}
    ]

    # Agrupar os dicionários
    lista_agrupada = agrupar_por_chaves(lista_dict_2)
    print(len(lista_agrupada))

    # Exibir o resultado
    pprint(lista_agrupada[0])