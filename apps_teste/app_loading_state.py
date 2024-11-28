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
    ],
    style={"padding": "20px"},
)


@app.callback(
    Output("output", "children"),
    Input("btn-processar", "n_clicks"),
    State("dropdown", "value"),
)
def processar(n_clicks, value):
    if not n_clicks:
        return "Clique no botão após selecionar uma opção no dropdown."

    if not value:
        return "Selecione uma opção antes de processar."

    # Simulando um tempo de processamento
    time.sleep(2)

    return f"Você selecionou: {value}"


if __name__ == "__main__":
    app.run_server(debug=True, port=8054)
