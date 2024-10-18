import dash
from dash import dcc, html, Input, Output, State, callback_context, ALL
from collections import defaultdict
import datetime

# 1) Input de dados ----------------------------------------------------------------------------------------------------

lista_teste = [
    {'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime.datetime(2024, 10, 17, 10, 45, 57, 889000), 'empresa': 'Parque Solar 1', 'tipo': 'dre',
     'parte': 1},
    {'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime.datetime(2024, 10, 17, 10, 45, 57, 928000), 'empresa': 'Parque Solar 1', 'tipo': 'dre',
     'parte': 2},
    {'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime.datetime(2024, 10, 17, 10, 45, 57, 967000), 'empresa': 'Parque Solar 1', 'tipo': 'dre',
     'parte': 3},
    {'nome': 'Cenário 2', 'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime.datetime(2024, 10, 17, 10, 45, 58, 11000), 'empresa': 'Parque Solar 1', 'tipo': 'dre',
     'parte': 4},
    {'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime.datetime(2024, 10, 17, 10, 46, 25, 804000), 'empresa': 'Parque Solar 1', 'tipo': 'dre',
     'parte': 1},
    {'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime.datetime(2024, 10, 17, 10, 46, 25, 847000), 'empresa': 'Parque Solar 1', 'tipo': 'dre',
     'parte': 2},
    {'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime.datetime(2024, 10, 17, 10, 46, 25, 889000), 'empresa': 'Parque Solar 1', 'tipo': 'dre',
     'parte': 3},
    {'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime.datetime(2024, 10, 17, 10, 46, 25, 936000), 'empresa': 'Parque Solar 1', 'tipo': 'dre',
     'parte': 4},
    {'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime.datetime(2024, 10, 17, 10, 47, 48, 514000), 'empresa': 'Parque Solar 1', 'tipo': 'bp',
     'parte': 1},
    {'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime.datetime(2024, 10, 17, 10, 47, 48, 563000), 'empresa': 'Parque Solar 1', 'tipo': 'bp',
     'parte': 2},
    {'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime.datetime(2024, 10, 17, 10, 47, 48, 612000), 'empresa': 'Parque Solar 1', 'tipo': 'bp',
     'parte': 3},
    {'nome': 'Cenário 1', 'descricao': 'Cenário de venda de parques solares + 5%',
     'data': datetime.datetime(2024, 10, 17, 10, 47, 48, 667000), 'empresa': 'Parque Solar 1', 'tipo': 'bp', 'parte': 4}
]


# 2) Funções -----------------------------------------------------------------------------------------------------------

# Função para agrupar os dicionários
def agrupar_por_chaves(lista_dicionarios) -> list[list[dict]]:
    grupos = defaultdict(list)

    for dicionario in lista_dicionarios:
        chave = (dicionario['nome'], dicionario['descricao'], dicionario['empresa'], dicionario['tipo'])
        grupos[chave].append(dicionario)

    lista: list[list[dict]] = list(grupos.values())
    # print(lista)  # debug

    return lista


# Função para criar os cards
def cards_cenarios_salvos(lista):
    return html.Div(
        className="div-content",
        children=[
            html.Div(
                id=f'div-{i}',
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
                                     "url('/assets/img/eolicas.jpg')",
                       'backgroundSize': 'cover',
                       'backgroundPosition': 'center',
                       'border-radius': '10px'
                       }
            ) for i, d in enumerate(lista)
        ], style={'display': 'flex',
                  'flexDirection': 'space-around',
                  'border': '1px solid gold',
                  'padding': '10px'}
    )


# Função para criar a lista de divs
def lista_cards_divs(lista_agrupada):
    divs = [html.Div(cards_cenarios_salvos(grupo), style={'border': '2px solid gold', 'marginBottom': '20px'})
            for grupo in lista_agrupada]
    return divs


# 3) Aplicativo Dash --------------------------------------------------------------------------------------------------

# Criação do aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    dcc.Store(id='store-data', data=lista_teste),  # Simulação dos cenários no dcc.Store
    html.Div(id='cards-container')
])


# 4) Callbacks ---------------------------------------------------------------------------------------------------------

# 4.1) Atualiza os cards na página -------------------------------------------------------------------------------------
@app.callback(
    Output(component_id='cards-container', component_property='children'),
    Input(component_id='store-data', component_property='data')
)
def update_cards(cenarios):
    if not cenarios:  # Verifica se a lista está vazia
        return "Nenhum cenário encontrado."  # Mensagem de fallback

    lista_agrupada = agrupar_por_chaves(cenarios)
    lista_divs_cards = lista_cards_divs(lista_agrupada)

    return lista_divs_cards


# 4.2) Callback para excluir um card -----------------------------------------------------------------------------------
@app.callback(
    Output(component_id='store-data', component_property='data'),
    Input(component_id={'type': 'delete-button', 'nome': ALL, 'descricao': ALL, 'empresa': ALL, 'tipo': ALL,
                        'parte': ALL}, component_property='n_clicks'),
    State(component_id='store-data', component_property='data'),
    prevent_initial_call=True
)
def delete_card(n_clicks, data):
    ctx = callback_context
    # print(ctx.triggered)  # debug
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    button_info = ctx.triggered[0]['prop_id'].split('.')[0].replace("'", "").replace('"', "")
    # print(button_info)  # debug

    nome, descricao, empresa, tipo, parte = button_info.split(",")[1:]
    # print(nome, descricao, empresa, tipo, parte)  # debug

    # Filtra a lista, removendo o item correspondente
    data = [d for d in data if not (
                d['nome'] == nome and d['descricao'] == descricao and d['empresa'] == empresa and d['tipo'] == tipo and
                d['parte'] == int(parte))]

    return data


if __name__ == '__main__':
    app.run_server(debug=True, port=8021)



