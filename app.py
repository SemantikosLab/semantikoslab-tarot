from dash import Dash, html
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Tarot SemantikosLab 🔮", style={'textAlign': 'center'}),
    html.P("Deuxième application Dash hébergée sur ton VPS OVH.",
           style={'textAlign': 'center'}),
    html.P("Sous-domaine : tarot-semantikoslab.amandinevelt.fr",
           style={'textAlign': 'center', 'fontStyle': 'italic'})
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8051)
