# Ce script est indépendant de Dash.
# Il fait tout le travail : chargement des données, traitement NLP, génération de fichiers de sortie (graphe, stats…).
import pandas as pd
import json
from semantic_utils import build_graph, compute_embeddings

INPUT = "../data/Tarot_Deck_cleaned/tarot_description_FR.xlsx"
OUTPUT_GRAPH = "outputs/tarot_graph.json"
OUTPUT_STATS = "outputs/stats_summary.json"

def main():
    print("Lecture du fichier source...")
    df = pd.read_excel(INPUT)

    print("Calcul des embeddings et du graphe...")
    graph = build_graph(df)
    stats = compute_embeddings(df)

    print("Sauvegarde des résultats...")
    with open(OUTPUT_GRAPH, "w") as f:
        json.dump(graph, f, indent=2)
    with open(OUTPUT_STATS, "w") as f:
        json.dump(stats, f, indent=2)

    print("Analyse terminée avec succès.")

if __name__ == "__main__":
    main()

