#!/bin/bash
# ============================================================
# INSTALLATION COMPLETE - TAROT SEMANTIKOSLAB
# Auteur : Amandine Velt
# Domaine : tarot-semantikoslab.amandinevelt.fr
# Environnement : Ubuntu 24.04 LTS / VPS OVH
# ============================================================

set -e

echo "Installation de Tarot SemantikosLab sur le VPS..."

# ------------------------------------------------------------
# Préparation de l'environnement
# ------------------------------------------------------------
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip nginx certbot python3-certbot-nginx git ufw

# ------------------------------------------------------------
# Création du répertoire de travail
# ------------------------------------------------------------
sudo mkdir -p /opt/tarot-semantikoslab
sudo chown -R ubuntu:ubuntu /opt/tarot-semantikoslab
cd /opt/tarot-semantikoslab

# ------------------------------------------------------------
# Environnement virtuel et dépendances
# ------------------------------------------------------------
python3 -m venv venv
source venv/bin/activate
pip install dash gunicorn pandas plotly

# ------------------------------------------------------------
# Application Dash
# ------------------------------------------------------------
cat > app.py <<'EOF'
from dash import Dash, html

app = Dash(__name__)
server = app.server

app.title = "Tarot SemantikosLab"

app.layout = html.Div([
    html.H1("Tarot SemantikosLab 🔮", style={'textAlign': 'center'}),
    html.P("Deuxième application Dash hébergée sur le VPS OVH.",
           style={'textAlign': 'center'}),
    html.P("Sous-domaine : tarot-semantikoslab.amandinevelt.fr",
           style={'textAlign': 'center', 'fontStyle': 'italic'})
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8051)
EOF

# ------------------------------------------------------------
# Service systemd pour Gunicorn
# ------------------------------------------------------------
sudo tee /etc/systemd/system/tarot-semantikoslab.service > /dev/null <<'EOF'
[Unit]
Description=Gunicorn instance for Tarot SemantikosLab
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/tarot-semantikoslab
Environment="PATH=/opt/tarot-semantikoslab/venv/bin"
ExecStart=/opt/tarot-semantikoslab/venv/bin/gunicorn -b 127.0.0.1:8051 app:server

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable tarot-semantikoslab
sudo systemctl start tarot-semantikoslab

# ------------------------------------------------------------
# Configuration Nginx (HTTP + HTTPS)
# ------------------------------------------------------------
sudo tee /etc/nginx/sites-available/tarot-semantikoslab > /dev/null <<'EOF'
server {
    server_name tarot-semantikoslab.amandinevelt.fr;

    listen 80;
    listen [::]:80;
    return 301 https://$host$request_uri;
}

server {
    server_name tarot-semantikoslab.amandinevelt.fr;

    listen 443 ssl;
    listen [::]:443 ssl;
    ssl_certificate /etc/letsencrypt/live/tarot-semantikoslab.amandinevelt.fr/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tarot-semantikoslab.amandinevelt.fr/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://127.0.0.1:8051;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/tarot-semantikoslab /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# ------------------------------------------------------------
# Certificat SSL Let's Encrypt
# ------------------------------------------------------------
sudo certbot --nginx -d tarot-semantikoslab.amandinevelt.fr --non-interactive --agree-tos -m contact@amandinevelt.fr

# ------------------------------------------------------------
# Sécurité (pare-feu)
# ------------------------------------------------------------
sudo ufw allow 'Nginx Full'
sudo ufw enable

# ------------------------------------------------------------
# Vérification finale
# ------------------------------------------------------------
echo "Vérification du service :"
sudo systemctl status tarot-semantikoslab --no-pager
echo "Vérification du site : https://tarot-semantikoslab.amandinevelt.fr"

echo "Installation complète terminée !"
