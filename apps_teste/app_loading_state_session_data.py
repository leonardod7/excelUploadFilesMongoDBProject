import dash
from dash import html, dcc, Input, Output, State
import time

# Inicializando o app
app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Exemplo de Dropdown com Loading Spinner"),
        dcc.Dropdown(
            id="dropdown",
            options=[
                {"label": "Opção 1", "value": "Opção 1"},
                {"label": "Opção 2", "value": "Opção 2"},
                {"label": "Opção 3", "value": "Opção 3"},
            ],
            placeholder="Selecione uma opção",
            style={"width": "50%"},
        ),
        html.Button("Processar", id="btn-processar", style={"marginTop": "20px"}),
        dcc.Loading(
            id="loading",
            type="circle",  # Tipos disponíveis: "default", "circle", "dot"
            children=html.Div(id="output", style={"marginTop": "20px"}),
        ),
        # Componente Store para manter os resultados após atualização da página
        dcc.Store(id="store", storage_type="session"),  # Usando "session" para armazenamento por sessão
    ],
    style={"padding": "20px"},
)

@app.callback(
    Output("store", "data"),  # Armazenando os resultados na sessão
    Output("output", "children"),  # Exibindo os resultados na tela
    Input("btn-processar", "n_clicks"),
    State("dropdown", "value"),
    State("store", "data"),  # Para recuperar os dados da sessão
)
def processar(n_clicks, value, stored_data):
    # Verificar se a página foi carregada ou se o botão foi pressionado
    if not n_clicks:
        if stored_data:
            return stored_data, stored_data["message"]
        return None, "Clique no botão após selecionar uma opção no dropdown."

    if not value:
        return stored_data, "Selecione uma opção antes de processar."

    # Simulando um tempo de processamento
    time.sleep(2)

    result = f"Você selecionou: {value}"

    # Armazenando o resultado no Store e retornando a mensagem
    return {"message": result}, result


if __name__ == "__main__":
    app.run_server(debug=True, port=8021)


