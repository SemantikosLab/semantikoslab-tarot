from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
import networkx as nx
import os

# === CONFIGURATION DE BASE ===
external_stylesheets = [dbc.themes.ZEPHYR]
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server
app.title = "Tarot SemantikosLab 🔮"

# === CHEMINS DES DONNÉES ===
DATA_PATH_FR = "data/Tarot_Deck_cleaned/tarot_description_FR.xlsx"
DATA_PATH_EN = "data/Tarot_Deck_cleaned/tarot_description_EN.xlsx"
GRAPH_PATH = "analysis/outputs/tarot_graph.json"
IMAGES_DIR = "assets/Cards"

# === INITIALISATION DES DONNÉES ===
df = pd.DataFrame()
G = nx.Graph()
try:
    with open(GRAPH_PATH) as f:
        graph_data = json.load(f)
        G = nx.node_link_graph(graph_data)
except Exception as e:
    print(f"Graphe non disponible : {e}")

# === BARRE DE NAVIGATION MULTILINGUE ===
def make_navbar(lang="FR"):
    if lang == "EN":
        nav_items = [
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Cards", href="/cards")),
            dbc.NavItem(dbc.NavLink("Semantic Analysis", href="/semantic")),
            dbc.NavItem(dbc.NavLink("Symbolic Graph", href="/graph")),
            dbc.NavItem(dbc.NavLink("Statistics", href="/stats")),
        ]
    else:
        nav_items = [
            dbc.NavItem(dbc.NavLink("Accueil", href="/")),
            dbc.NavItem(dbc.NavLink("Cartes", href="/cards")),
            dbc.NavItem(dbc.NavLink("Analyse sémantique", href="/semantic")),
            dbc.NavItem(dbc.NavLink("Graphe symbolique", href="/graph")),
            dbc.NavItem(dbc.NavLink("Statistiques", href="/stats")),
        ]

    # === Dropdown de sélection de langue ===
    lang_dropdown = dbc.DropdownMenu(
        label="🇫🇷 Français" if lang == "FR" else "🇬🇧 English",
        children=[
            dbc.DropdownMenuItem("🇫🇷 Français", id="lang-fr"),
            dbc.DropdownMenuItem("🇬🇧 English", id="lang-en")
        ],
        nav=True,
        in_navbar=True,
        align_end=True,
    )

    return dbc.NavbarSimple(
        brand="Tarot SemantikosLab 🔮",
        color="dark",
        dark=True,
        brand_style={"fontWeight": "bold", "letterSpacing": "1px"},
        children=nav_items + [lang_dropdown],
        fluid=True,
    )

# === PAGE D'ACCUEIL ===
def make_home_page(lang="FR"):
    if lang == "EN":
        title = "☽ Tarot SemantikosLab ☾"
        subtitle1 = "A laboratory of semantic and symbolic exploration of the Rider–Waite Tarot, where each card becomes a node in a network of meanings."
        subtitle2 = "Between word and symbol, a map of consciousness emerges — at the crossroads of linguistics, mythology, and artificial intelligence."
        goal = "Explore semantic relations between major and minor arcana using NLP and knowledge graphs."
        footer = "© 2025 Amandine Velt — SemantikosLab"
    else:
        title = "☽ Tarot SemantikosLab ☾"
        subtitle1 = "Laboratoire d’exploration sémantique et symbolique du Tarot de Rider–Waite, où chaque carte devient un nœud dans un réseau de significations."
        subtitle2 = "Entre le mot et le symbole, une cartographie de la conscience se dessine — à la croisée de la linguistique, de la mythologie et de l’intelligence artificielle."
        goal = "Explorer les relations sémantiques entre les arcanes majeurs et mineurs grâce au NLP et aux graphes de connaissance."
        footer = "© 2025 Amandine Velt — SemantikosLab"

    return dbc.Container([
        html.Div([
            html.H2(title, className="text-center mt-4 mb-3 fw-bold fade-in", style={"color": "#2f2640"}),
            html.P(subtitle1, className="text-center mb-4 fst-italic fade-in", style={"opacity": 0.9}),
            html.P(subtitle2, className="text-center mb-5 fade-in", style={"color": "#4a3e6b"}),
            dbc.Card(
                dbc.CardBody([
                    html.H4("Goal" if lang == "EN" else "Objectif", className="card-title mb-3"),
                    html.P(goal),
                ]),
                className="shadow-sm mx-auto fade-in",
                style={"maxWidth": "700px", "textAlign": "center",
                       "backgroundColor": "rgba(255,255,255,0.9)",
                       "borderRadius": "15px"}
            ),
            html.Footer(footer, className="text-center mt-5 mb-3 fade-in",
                        style={"color": "#6b5c7a", "fontSize": "14px"}),
        ])
    ])

# === AUTRES PAGES ===
def make_cards_page(df, lang="FR"):
    label = "Sélectionner une carte :" if lang == "FR" else "Select a card:"
    return dbc.Container([
        html.H3("Explorateur de cartes" if lang == "FR" else "Tarot Cards Explorer",
                className="text-center mt-4 mb-4 fw-bold fade-in"),
        dbc.Row([
            dbc.Col([
                html.Label(label, className="fw-bold fade-in"),
                dcc.Dropdown(
                    id="card-dropdown",
                    options=[{"label": n, "value": n} for n in df["card"].unique()],
                    value=df["card"].iloc[0] if not df.empty else None,
                    clearable=False,
                    style={"width": "100%"}
                ),
            ], md=4),
            dbc.Col([
                html.Div(id="card-info", className="p-3 shadow-sm fade-in",
                         style={"backgroundColor": "rgba(255,255,255,0.95)",
                                "borderRadius": "10px", "minHeight": "250px"})
            ], md=8),
        ], className="mt-4")
    ])

def make_semantic_page(df, lang="FR"):
    title = "Analyse sémantique des cartes" if lang == "FR" else "Semantic Analysis of Cards"
    label_card = "Choisir une carte :" if lang == "FR" else "Choose a card:"
    label_len = "Filtrer par longueur minimale :" if lang == "FR" else "Filter by minimum length:"
    return dbc.Container([
        html.H3(title, className="text-center mt-4 mb-4 fw-bold fade-in"),
        dbc.Row([
            dbc.Col([
                html.Label(label_card, className="fade-in"),
                dcc.Dropdown(
                    id="card-select",
                    options=[{"label": c, "value": c} for c in df["card"].unique()],
                    value=df["card"].iloc[0] if not df.empty else None
                ),
                html.Br(),
                html.Label(label_len, className="fade-in"),
                dcc.Slider(0, 500, 10, value=100, id="len-slider")
            ], md=3),
            dbc.Col([dcc.Graph(id="semantic-graph", className="fade-in")], md=9)
        ])
    ])

graph_page = dbc.Container([
    html.H3("Graphe symbolique / Symbolic Graph", className="text-center mt-4 mb-4 fw-bold fade-in"),
    dcc.Graph(id="network-graph", className="fade-in"),
])

def make_stats_page(df, lang="FR"):
    title = "Statistiques globales" if lang == "FR" else "Global Statistics"
    desc = "Distribution de la longueur des descriptions :" if lang == "FR" else "Distribution of description lengths:"
    return dbc.Container([
        html.H3(title, className="text-center mt-4 mb-4 fw-bold fade-in"),
        html.P(desc, className="mb-3 fade-in"),
        dcc.Graph(
            figure=px.histogram(
                df, x=df["description"].str.len(),
                nbins=30, color_discrete_sequence=["#a29bfe"]
            ).update_layout(template="plotly_dark"),
            className="fade-in"
        )
    ])

# === CALLBACKS ===
@app.callback(
    Output("card-info", "children"),
    Input("card-dropdown", "value")
)
def update_card_info(selected_card):
    if df.empty or not selected_card:
        return html.P("Aucune donnée disponible / No data available.", className="text-muted fade-in")

    card = df[df["card"] == selected_card].iloc[0]
    img_filename = str(card["img"]).strip()
    img_src = f"/assets/Cards/{img_filename}" if img_filename else None

    return dbc.Row([
        dbc.Col([
            html.Img(src=img_src, className="fade-in",
                     style={"maxWidth": "100%", "borderRadius": "10px",
                            "boxShadow": "0 2px 6px rgba(0,0,0,0.2)"})
            if img_filename else html.P("Image not found.", className="text-muted fade-in")
        ], md=4),
        dbc.Col([
            html.H4(card["card"], className="fw-bold mb-3 fade-in"),
            html.P(card["description"], style={"fontStyle": "italic"}),
            html.Hr(),
            html.P(f"Keywords: {card['keywords_general']}"),
            html.P(f"Upright: {card['keywords_upright']}"),
            html.P(f"Reversed: {card['keywords_reversed']}")
        ], md=8)
    ])

@app.callback(
    Output("semantic-graph", "figure"),
    Input("card-select", "value"),
    Input("len-slider", "value")
)
def update_semantic_graph(selected_card, min_len):
    if df.empty:
        return {}
    subset = df[df["description"].str.len() > min_len]
    fig = px.scatter(subset, x=range(len(subset)), y=subset["description"].str.len(),
                     hover_name=subset["card"], color=subset["card"] == selected_card,
                     color_discrete_sequence=["#a29bfe", "#ffeaa7"])
    fig.update_layout(template="plotly_dark", title=f"Analyse : {selected_card}")
    return fig

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

# === CHOIX DE LANGUE ===
@app.callback(
    Output("language-store", "data"),
    Input("lang-fr", "n_clicks"),
    Input("lang-en", "n_clicks"),
    prevent_initial_call=True
)
def set_language(fr_click, en_click):
    if fr_click:
        return "FR"
    elif en_click:
        return "EN"
    raise dash.exceptions.PreventUpdate  # ✅ ne rien faire si aucun clic

# === ROUTAGE DES PAGES ===
@app.callback(
    Output("page-content", "children"),
    Output("navbar", "children"),
    Input("url", "pathname"),
    Input("language-store", "data")
)
def display_page(pathname, lang):
    global df

    # ✅ NE PAS repasser en FR si 'lang' est None
    # on attend que le store soit prêt
    if lang not in ["FR", "EN"]:
        raise dash.exceptions.PreventUpdate

    try:
        df = pd.read_excel(DATA_PATH_EN if lang == "EN" else DATA_PATH_FR)
    except Exception as e:
        print(f"Erreur de chargement : {e}")
        df = pd.DataFrame()

    navbar = make_navbar(lang)

    if pathname == "/semantic":
        return make_semantic_page(df, lang), navbar
    elif pathname == "/graph":
        return graph_page, navbar
    elif pathname == "/stats":
        return make_stats_page(df, lang), navbar
    elif pathname == "/cards":
        return make_cards_page(df, lang), navbar
    else:
        return make_home_page(lang), navbar

# === LAYOUT GLOBAL ===
app.layout = html.Div([
    dcc.Store(id="language-store", storage_type="local"),
    dcc.Location(id="url"),
    html.Div(id="navbar", children=make_navbar("FR")),
    html.Div(id="page-content", children=make_home_page("FR"))
])

# === LANCEMENT ===
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8051, debug=False)
