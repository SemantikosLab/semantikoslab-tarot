from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
import networkx as nx

# === CONFIGURATION DE BASE ===
external_stylesheets = [dbc.themes.ZEPHYR]
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server
app.title = "Tarot SemantikosLab 🔮"

# === CHARGEMENT DES DONNÉES ===
DATA_PATH = "data/Tarot_Deck_cleaned/tarot_cards_description_cleaned.xlsx"
GRAPH_PATH = "analysis/outputs/tarot_graph.json"

try:
    df = pd.read_excel(DATA_PATH)
    with open(GRAPH_PATH) as f:
        graph_data = json.load(f)
        G = nx.node_link_graph(graph_data)
except Exception as e:
    print(f"Données non disponibles : {e}")
    df, G = pd.DataFrame(), nx.Graph()

# === BARRE DE NAVIGATION ===
navbar = dbc.NavbarSimple(
    brand="Tarot SemantikosLab 🔮",
    color="dark",
    dark=True,
    brand_style={"fontWeight": "bold", "letterSpacing": "1px"},
    children=[
        dbc.NavItem(dbc.NavLink("Accueil", href="/")),
        dbc.NavItem(dbc.NavLink("Analyse sémantique", href="/semantic")),
        dbc.NavItem(dbc.NavLink("Graphe symbolique", href="/graph")),
        dbc.NavItem(dbc.NavLink("Statistiques", href="/stats")),
    ],
    fluid=True,
)

# === PAGE D'ACCUEIL ===
home_page = dbc.Container([
    html.Div([
        html.H2("☽ Tarot SemantikosLab ☾", className="text-center mt-4 mb-3 fw-bold",
                style={"color": "#2f2640"}),
        html.P(
            "Laboratoire d’exploration sémantique et symbolique du Tarot de Rider–Waite, "
            "où chaque carte devient un nœud dans un réseau de significations.",
            className="text-center mb-4 fst-italic",
            style={"opacity": 0.9}
        ),
        html.P(
            "Entre le mot et le symbole, une cartographie de la conscience se dessine — "
            "à la croisée de la linguistique, de la mythologie et de l’intelligence artificielle.",
            className="text-center mb-5",
            style={"color": "#4a3e6b"}
        ),
        dbc.Card(
            dbc.CardBody([
                html.H4("Objectif", className="card-title mb-3"),
                html.P("Explorer les relations sémantiques entre les arcanes majeurs et mineurs "
                       "grâce au traitement automatique du langage (NLP) et aux graphes de connaissance."),
            ]),
            className="shadow-sm mx-auto",
            style={"maxWidth": "700px", "textAlign": "center",
                   "backgroundColor": "rgba(255,255,255,0.9)",
                   "borderRadius": "15px"}
        ),
        html.Footer("© 2025 Amandine Velt — SemantikosLab",
                    className="text-center mt-5 mb-3",
                    style={"color": "#6b5c7a", "fontSize": "14px"}),
    ])
])

# === PAGE ANALYSE SÉMANTIQUE ===
semantic_page = dbc.Container([
    html.H3("Analyse sémantique des cartes", className="text-center mt-4 mb-4 fw-bold"),
    dbc.Row([
        dbc.Col([
            html.Label("Choisir une carte :"),
            dcc.Dropdown(
                id="card-select",
                options=[{"label": c, "value": c} for c in df["name"].unique()],
                value=df["name"].iloc[0] if not df.empty else None
            ),
            html.Br(),
            html.Label("Filtrer par longueur minimale :"),
            dcc.Slider(0, 500, 10, value=100, id="len-slider")
        ], md=3),

        dbc.Col([
            dcc.Graph(id="semantic-graph")
        ], md=9)
    ])
])

@app.callback(
    Output("semantic-graph", "figure"),
    Input("card-select", "value"),
    Input("len-slider", "value")
)
def update_semantic_graph(selected_card, min_len):
    if df.empty:
        return {}
    subset = df[df["summary_text"].str.len() > min_len]
    fig = px.scatter(subset, x=range(len(subset)), y=subset["summary_text"].str.len(),
                     hover_name=subset["name"], color=subset["name"] == selected_card,
                     color_discrete_sequence=["#a29bfe", "#ffeaa7"])
    fig.update_layout(template="plotly_dark", title=f"Analyse sémantique : {selected_card}")
    return fig

# === PAGE GRAPHE SYMBOLIQUE ===
graph_page = dbc.Container([
    html.H3("Graphe symbolique des arcanes", className="text-center mt-4 mb-4 fw-bold"),
    dcc.Graph(id="network-graph"),
])

@app.callback(Output("network-graph", "figure"), Input("network-graph", "id"))
def display_graph(_):
    if G.number_of_nodes() == 0:
        return {}
    pos = nx.spring_layout(G, seed=42)
    edge_x, edge_y, node_x, node_y = [], [], [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
    fig = px.scatter(x=node_x, y=node_y, text=list(G.nodes()), color_discrete_sequence=["#70a8ff"])
    fig.add_scatter(x=edge_x, y=edge_y, mode="lines", line=dict(color="rgba(112,168,255,0.3)", width=1))
    fig.update_traces(textposition="top center")
    fig.update_layout(template="plotly_dark", showlegend=False)
    return fig

# === PAGE STATISTIQUES ===
stats_page = dbc.Container([
    html.H3("Statistiques globales", className="text-center mt-4 mb-4 fw-bold"),
    html.P("Distribution de la longueur des descriptions des cartes :", className="mb-3"),
    dcc.Graph(
        figure=px.histogram(
            df, x=df["summary_text"].str.len(),
            nbins=30, title="Longueur des descriptions (caractères)",
            color_discrete_sequence=["#a29bfe"]
        ).update_layout(template="plotly_dark")
    )
])

# === ROUTAGE DES PAGES ===
app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    html.Div(id="page-content")
])

@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/semantic":
        return semantic_page
    elif pathname == "/graph":
        return graph_page
    elif pathname == "/stats":
        return stats_page
    else:
        return home_page

# === LANCEMENT ===
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8051, debug=False)

