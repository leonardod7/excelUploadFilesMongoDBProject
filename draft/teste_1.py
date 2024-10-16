import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# Inicializando a aplicação
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sidebar layout
sidebar = html.Div(
    [
        html.Button("+ Create Database", className="btn btn-primary mb-3"),
        html.Div(
            [
                dcc.Input(
                    placeholder="Search Namespaces",
                    type="text",
                    className="form-control"
                )
            ],
            className="mb-3"
        ),
        html.Div(
            [
                html.H5("Eólicas", className="sidebar-heading"),
                html.Ul(
                    [
                        html.Li("SPE Boi Gordo", className="nav-item"),
                        html.Li("SPE Moinhos de Vento", className="nav-item")
                    ],
                    className="nav flex-column"
                )
            ],
            className="sidebar-section"
        )
    ],
    className="sidebar"
)

# Main content layout
content = html.Div(
    [
        html.Div(
            [
                html.H3("Eólicas.SPE Boi Gordo"),
                html.P("STORAGE SIZE: 456KB  |  LOGICAL DATA SIZE: 2.74MB  |  TOTAL DOCUMENTS: 4"),
                html.A("Generate queries from natural language in Compass", href="#", className="btn-link"),
            ],
            className="content-header"
        ),
        html.Div(
            [
                dcc.Input(
                    placeholder='Type a query: { field: "value" }',
                    type='text',
                    className="form-control mb-2"
                ),
                html.Div(
                    [
                        html.Button("Reset", className="btn btn-secondary me-2"),
                        html.Button("Apply", className="btn btn-success"),
                        html.A("Options", href="#", className="btn-link ms-2")
                    ]
                )
            ],
            className="search-filter"
        ),
        html.Div(
            [
                html.H5("QUERY RESULTS: 1-1 OF MANY"),
                html.Pre(
                    '''
                    {
                        "_id": ObjectId("670d1060a35664b5a885e2a1"),
                        "nome": "Cenário 1",
                        "descricao": "Cenário com investimento em novos parques eólicos, variando 15%",
                        "data": "2024-10-14T09:36:48.367+00:00",
                        "setor": "eolicas",
                        "empresa": "SPE Boi Gordo",
                        "dre": Array(6000),
                        "tipo": "dre",
                        "parte": 1
                    }
                    ''',
                    className="json-result"
                )
            ],
            className="query-results"
        )
    ],
    className="content"
)

# Final Layout
app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=3),
                dbc.Col(content, width=9)
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8012)
