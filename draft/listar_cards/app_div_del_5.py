import dash
from dash import dcc, html, Input, Output, State, callback_context, ALL
import datetime
from collections import defaultdict
from pprint import pprint


lista_teste: list[dict] = [
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


def cards_cenarios_salvos(lista: list[dict]) -> html.Div:
    conteudo: html.Div = html.Div(
        className="div-content",
        children=[
            # Div das informações
            html.Div(
                id=f'div-{i}',  # Agora o id é único, pois usa o índice `i`
                children=[
                    html.H4(children=[d['nome']],
                            style={'fontFamily': 'Arial Narrow',
                                   'fontSize': '14px',
                                   'borderBottom': '2px solid gray',
                                   'paddingBottom': '5px',
                                   'marginTop': '5px',
                                   'border-radius': '5px'}),

                    html.P(children=[
                        html.Span(children=["Empresa: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                        f"{d['empresa']}"], style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

                    html.P(children=[
                        html.Span(children=["Descrição: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                        f"{d['descricao']}"], style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

                    html.P(children=[
                        html.Span(children=["Data: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                        f"{d['data']}"], style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

                    html.P(children=[
                        html.Span(children=["Tipo: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                        f"{d['tipo']}"], style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

                    html.P(children=[
                        html.Span(children=["Parte: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                        f"{d['parte']}"], style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

                    html.Button(children=['🗑️'], id={'type': 'delete-button', 'nome': d['nome'],
                                                     'descricao': d['descricao'],
                                                     'empresa': d['empresa'],
                                                     'tipo': d['tipo'],
                                                     'parte': d['parte']}, n_clicks=0)
                ],
                style={'border': '1px solid #ccc',
                       'margin': '10px',
                       'padding': '10px',
                       'width': '300px',
                       'background': "linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), "
                                     "url('/assets/img/eolicas.jpg')",  # Aplicando transparência na imagem
                       'backgroundSize': 'cover',  # Ajusta a imagem para cobrir a div
                       'backgroundPosition': 'center',  # Centraliza a imagem
                       'border-radius': '10px'
                       }
            ) for i, d in enumerate(lista)
        ], style={'display': 'flex',
                  'flexDirection': 'space-around',
                  'border': '1px solid gold',
                  'padding': '10px'}
    )

    # print(f"Button ID: {{'type': 'delete-button', 'nome': d['nome'], 'descricao': d['descricao'], "
    #       f"'empresa': d['empresa'], 'tipo': d['tipo'], 'parte': d['parte']}}")  # debug

    return conteudo


def lista_cards_divs(lista_agrupada: list[list[dict]]) -> list[html.Div]:
    divs = [html.Div(cards_cenarios_salvos(lista=grupo), style={'border': '2px solid gold', 'marginBottom': '20px'})
            for grupo in lista_agrupada]
    return divs


# Criação do aplicativo Dash
app = dash.Dash(__name__)

lista_agrupada = agrupar_por_chaves(lista_teste)

# Layout do aplicativo ------------------------------------------------------------------------------------------------
# Layout do aplicativo ------------------------------------------------------------------------------------------------
app.layout = html.Div([
    dcc.Store(id='store-data', data=lista_teste),  # Simulação dos cenários no dcc.Store
    html.Div(id='cards-container')
])

# Atualiza os cards na página
@app.callback(
    Output(component_id='cards-container', component_property='children'),
    Input(component_id='store-data', component_property='data')
)
def update_cards(cenarios):
    print("Atualizando os cards.....")  # debug
    lista_agrupada = agrupar_por_chaves(cenarios)  # Agrupa os cenários por chave
    return lista_cards_divs(lista_agrupada)  # Renderiza as divs para cada grupo


# Deleta um card
@app.callback(
    Output(component_id='store-data', component_property='data'),
    Input(component_id={'type': 'delete-button', 'nome': ALL, 'descricao': ALL,
                        'empresa': ALL, 'tipo': ALL, 'parte': ALL}, component_property='n_clicks'),
    State(component_id='store-data', component_property='data'),
    prevent_initial_call=True
)
def delete_card(n_clicks, data):
    ctx = callback_context

    # Verifica se algum botão foi acionado
    if not ctx.triggered or all(click is None for click in n_clicks):
        print("Nenhum botão foi acionado.")
        return dash.no_update

    # Obtém o ID do botão que foi clicado
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    button_id_dict = eval(button_id)

    print(f"Button ID: {button_id_dict}")  # Adicione este print aqui

    # Encontra o cartão correspondente ao ID do botão
    card_to_delete = {
        'nome': button_id_dict['nome'],
        'descricao': button_id_dict['descricao'],
        'empresa': button_id_dict['empresa'],
        'tipo': button_id_dict['tipo'],
        'parte': button_id_dict['parte']
    }

    # Remove o cartão correspondente da lista de dados
    new_data = [d for d in data if d != card_to_delete]

    return new_data


if __name__ == '__main__':
    app.run(debug=True, port=8987)