cenarios = [{'id': 'abfa37ae-3bc7-4587-96c0-a8f2658f9466', 'cenario': 'Cenário 1', 'empresa': 'Parque Solar 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17T10:45:57.889000', 'tipo': 'dre', 'parte': 1}, {'id': '9b78062e-e436-4e23-832a-3771f0e18d11', 'cenario': 'Cenário 1', 'empresa': 'Parque Solar 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17T10:45:57.928000', 'tipo': 'dre', 'parte': 2}, {'id': '01c4a879-266b-4186-8bb1-d14b745f4955', 'cenario': 'Cenário 1', 'empresa': 'Parque Solar 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17T10:45:57.967000', 'tipo': 'dre', 'parte': 3}, {'id': 'b99a1bcd-289b-4f0f-a19f-6e861fdf9538', 'cenario': 'Cenário 1', 'empresa': 'Parque Solar 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17T10:45:58.011000', 'tipo': 'dre', 'parte': 4}, {'id': '2591eba6-3d71-495c-86fc-26563d1f0bce', 'cenario': 'Cenário 2', 'empresa': 'Parque Solar 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17T10:47:48.514000', 'tipo': 'bp', 'parte': 1}, {'id': 'c00e6b90-c8cc-4c5d-9589-9c203a118e7e', 'cenario': 'Cenário 2', 'empresa': 'Parque Solar 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17T10:47:48.563000', 'tipo': 'bp', 'parte': 2}, {'id': '9dc00eef-ece9-4ff4-bc20-f33c60da1001', 'cenario': 'Cenário 2', 'empresa': 'Parque Solar 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17T10:47:48.612000', 'tipo': 'bp', 'parte': 3}, {'id': '7059cc2a-67a6-45e8-974a-00497a1a2c84', 'cenario': 'Cenário 2', 'empresa': 'Parque Solar 1', 'descricao': 'Cenário de venda de parques solares + 5%', 'data': '2024-10-17T10:47:48.667000', 'tipo': 'bp', 'parte': 4}]
n_clicks = [0, 1, 0, 0, 0, 0, 0, 0]

# Identificar o índice do botão clicado
clicked_index = [i for i, click in enumerate(n_clicks) if click > 0][0]

# Obter o ID do cenário a ser deletado
card_id_to_delete = cenarios[clicked_index]["id"]

# Executar o app
if __name__ == "__main__":
    print('Index do botão clicado: -------------------')
    print(clicked_index)
    print('ID do Cenário clicado: -------------------')
    print(card_id_to_delete)
