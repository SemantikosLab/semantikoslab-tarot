# 🔮 SemantikosLab Tarot  
**Analyse sémantique et symbolique du Tarot — à la croisée du langage, des archétypes et de l’intelligence artificielle.**

---

## Présentation

**SemantikosLab Tarot** est une application de recherche et d’exploration sémantique du Tarot Rider–Waite.  
Elle relie les **symboles, les textes fondateurs et les archétypes universels** à travers des méthodes issues du **traitement automatique du langage (NLP)** et de l’**analyse de graphes de connaissances**.

Cette approche vise à étudier le Tarot non comme un outil divinatoire,  
mais comme un **langage vivant** — un miroir de la pensée humaine, de la mémoire collective et des civilisations.

> *« Entre le mot et le symbole, une cartographie de la civilisation humaine et de la conscience se dessine. »* 

---

## Objectifs du projet

- Construire une **base sémantique des 78 cartes du Tarot** (majeures et mineures)  
- Analyser leurs **liens linguistiques, symboliques et archétypaux**  
- Explorer la **cohérence entre le Tarot, les textes sacrés et la mythologie**  
- Expérimenter des **modèles de langage (LLM, embeddings, NLP)** appliqués aux traditions symboliques  
- Visualiser les relations entre cartes, concepts et émotions via des **graphes interactifs**

---

## Technologies principales

| Domaine | Bibliothèques clés |
|----------|--------------------|
| Web App | [Dash](https://dash.plotly.com), [Plotly](https://plotly.com/python/), [Dash Cytoscape](https://dash.plotly.com/cytoscape) |
| NLP | [spaCy](https://spacy.io), [sentence-transformers](https://www.sbert.net) |
| Graphes | [NetworkX](https://networkx.org), [PyVis](https://pyvis.readthedocs.io) |
| Hébergement | Ubuntu 24.04, Nginx, Gunicorn, Certbot |

---

## Installation locale

### 1. Cloner le dépôt
```bash
git clone git@github.com:SemantikosLab/semantikoslab-tarot.git
cd semantikoslab-tarot
```

### 2. Créer un environnement virtuel
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer l’application
```bash
python app.py
```

L’application sera accessible à l’adresse :
http://127.0.0.1:8050

### Structure

semantikoslab-tarot/
│
├── app.py                 → Application Dash principale
├── data/                  → Données textuelles, cartes, métadonnées
├── assets/                → Feuilles de style, thèmes et scripts
├── requirements.txt       → Dépendances Python
├── README.md              → Ce fichier
└── LICENSE

### Exemple d’analyse

L’application visualise les liens sémantiques entre les cartes du Tarot et leurs descriptions textuelles.
Chaque carte est intégrée dans un graphe de similarité conceptuelle, où la proximité des nœuds révèle des affinités symboliques.

### Liens connexes

https://semantikoslab.amandinevelt.fr/ – portail principal reliant les projets sémantiques
https://tarot-semantikoslab.amandinevelt.fr/ – application web de ce projet

### Auteure

Amandine Velt - SémantikosLab
