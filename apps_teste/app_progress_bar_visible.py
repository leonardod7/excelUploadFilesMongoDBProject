import dash
from dash import html, dcc, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import time

# Inicializando o app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        html.H1("Exemplo de Dropdown com Barra de Progresso"),
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
        dbc.Button("Processar", id="btn-processar", color="primary", className="mt-3"),
        html.Div(id="output", className="mt-3"),
        dbc.Progress(id="progress-bar", striped=True, animated=True, className="mt-3"),
        dcc.Interval(id="progress-interval", interval=500, n_intervals=0, disabled=True),
    ],
    style={"padding": "20px"},
)


@app.callback(
    [
        Output("progress-bar", "value"),
        Output("progress-bar", "label"),
        Output("progress-interval", "disabled"),
        Output("progress-interval", "n_intervals"),
        Output("output", "children"),
    ],
    [
        Input("progress-interval", "n_intervals"),
        Input("btn-processar", "n_clicks"),
    ],
    State("dropdown", "value"),
)
def handle_progress(n_intervals, n_clicks, value):
    ctx = callback_context

    # Verifica qual componente disparou o callback
    if not ctx.triggered:
        return dash.no_update, dash.no_update, True, dash.no_update, dash.no_update

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "btn-processar":
        # Verifica se foi clicado no botão sem valor selecionado no dropdown
        if value is None:
            return dash.no_update, dash.no_update, True, 0, "Selecione uma opção no dropdown antes de processar."

        # Reinicia o progresso e exibe a barra
        time.sleep(1)  # Simula um pequeno atraso inicial
        return 0, "0%", False, 0, dash.no_update

    elif triggered_id == "progress-interval":
        progress = n_intervals * 10

        if progress >= 100:
            return 100, "Concluído!", True, 0, f"Você selecionou: {value}"

        return progress, f"{progress}%", False, dash.no_update, dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True)

