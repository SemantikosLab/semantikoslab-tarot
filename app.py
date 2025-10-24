from dash import Dash, html
import dash_bootstrap_components as dbc

# 🌸 Thème clair et harmonieux
external_stylesheets = [dbc.themes.ZEPHYR]

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Tarot SemantikosLab 🔮"

# 🌙 Layout principal
app.layout = html.Div(
    [
        # 🔮 Image d’arrière-plan pulsante
        html.Div(className="bg-image"),

        # --- Contenu principal dans un cadre lavande translucide ---
        dbc.Container(
            html.Div(
                [
                    html.H1("🔮 Tarot SemantikosLab"),

                    html.P(
                        "Application d’analyse sémantique et symbolique du Tarot de Rider–Waite, "
                        "où les cartes deviennent des nœuds d’un réseau linguistique et archétypal.",
                    ),

                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(
                                    "✨ Interface en construction",
                                    className="card-title mb-3",
                                ),
                                html.P(
                                    "Cette application explorera les graphes sémantiques, "
                                    "les cooccurrences symboliques et les réseaux archétypaux "
                                    "des arcanes majeurs et mineurs.",
                                    className="card-text",
                                ),
                            ]
                        ),
                        className="shadow-sm mx-auto mt-4",
                        style={"maxWidth": "500px"},
                    ),

                    html.Footer("© 2025 Amandine Velt — SemantikosLab"),
                ],
                className="main-box",
                style={"marginTop": "10vh"},
            ),
            fluid=True,
            style={
                "position": "relative",
                "zIndex": "2",
                "minHeight": "100vh",
                "paddingBottom": "5vh",
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8051, debug=False)
