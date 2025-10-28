# analysis/run_analysis.py
# Script indépendant de Dash : calcule graphe + stats + wordclouds FR/EN

import json
import re
from pathlib import Path

import pandas as pd
from wordcloud import WordCloud, STOPWORDS

from semantic_utils import build_graph, compute_embeddings

# --- chemins ---
HERE = Path(__file__).resolve().parent                   # analysis/
ROOT = HERE.parent                                      # repo root
DATA_DIR = (HERE / ".." / "data" / "Tarot_Deck_cleaned").resolve()

DATA_FR = DATA_DIR / "tarot_description_FR.xlsx"
DATA_EN = DATA_DIR / "tarot_description_EN.xlsx"

OUTPUTS_DIR = ROOT / "analysis" / "outputs"
ASSETS_DIR = ROOT / "assets"  # Dash sert automatiquement ce dossier

OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# --- fichiers de sortie ---
GRAPH_FR = OUTPUTS_DIR / "tarot_graph_fr.json"
GRAPH_EN = OUTPUTS_DIR / "tarot_graph_en.json"
STATS_FR = OUTPUTS_DIR / "stats_summary_fr.json"
STATS_EN = OUTPUTS_DIR / "stats_summary_en.json"
WC_FR = ASSETS_DIR / "wordcloud_fr.png"
WC_EN = ASSETS_DIR / "wordcloud_en.png"
MANIFEST = OUTPUTS_DIR / "manifest.json"

# --- stopwords FR additionnels ---
STOP_FR_EXTRA = {
    "les","des","pour","avec","sans","dans","entre","ainsi","comme","plus",
    "aussi","afin","sous","sur","vers","chez","dont","cette","cet","cela",
    "celles","ceux","celui","celles-ci","ceci","lors","tandis","alors","être",
    "tout","toute","toutes","tous","lorsque","car","par","au","aux","du",
    "de","la","le","un","une","et","ou","se","sa","son","ses","leur","leurs",
    "elle","il","ils","elles","on","que","qui","quand", "à", "ton", "par", "te",
    "carte","symbolise","évoque","représente","invite","parle","indique",
    "en","vers","est","c’est","peut","souvent","met","après","tu","incarne","envers"
}

STOP_EN_EXTRA = {
    "card","reversed","shows","suggests","indicates","means",
    "represents","symbolize","bring","warns","message","tells",
    "this","that","can","often"
}

def normalize_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = re.sub(r"http\S+", " ", s)                       # URLs
    s = re.sub(r"[^\w’'\- ]+", " ", s, flags=re.UNICODE) # ponctuation
    s = re.sub(r"\s+", " ", s).strip()
    return s

def gather_corpus(df: pd.DataFrame) -> str:
    # Concatène description + mots-clés si présents
    cols = [c for c in df.columns if c.lower() in {
        "description","keywords_general","keywords_upright","keywords_reversed","reversed_meaning","upright_meaning"
    }]
    if cols:
        parts = [df[c].astype(str) for c in cols]
        all_text = " . ".join([" ".join(p) for p in parts])
    else:
        all_text = " ".join(df.astype(str).fillna("").agg(" ".join, axis=1))
    return normalize_text(all_text)

def make_wordcloud(text: str, lang_code: str, out_path: Path):
    # 1) normalisation légère
    if not isinstance(text, str):
        text = ""
    # normaliser apostrophes typographiques et minuscules
    text = text.replace("’", "'").lower()

    # 2) contractions spécifiques
    if lang_code.lower() == "fr":
        # enlever formes contractées FR communes
        for x in ["d'", "l'", "qu'", "n'", "s'", "j'", "t'", "m'", "c'"]:
            text = text.replace(x, " ")
    else:
        # enlever le possessif anglais
        text = text.replace("'s ", " ")

    # 3) stopwords
    sw = set(STOPWORDS)
    if lang_code.lower() == "en":
        sw |= STOP_EN_EXTRA
    elif lang_code.lower() == "fr":
        sw |= STOP_FR_EXTRA

    # 4) génération
    wc = WordCloud(
        width=1600,
        height=1000,
        background_color="white",
        stopwords=sw,
        collocations=True,   # conserve certaines bigrammes utiles
        max_words=300,
        random_state=42      # reproductible
        # font_path="assets/DejaVuSans.ttf",  # ← décommente si accents mal rendus
    ).generate(text)

    # 5) export
    wc.to_file(str(out_path))

def process_language(lang_label: str, xlsx_path: Path, out_graph: Path, out_stats: Path, out_wc: Path):
    print(f"[{lang_label}] Lecture :", xlsx_path)
    df = pd.read_excel(xlsx_path)

    # Wordcloud
    corpus = gather_corpus(df)
    print(f"[{lang_label}] Génération du wordcloud -> {out_wc}")
    make_wordcloud(corpus, lang_label.lower(), out_wc)

    # Graphe + stats
    print(f"[{lang_label}] Calcul du graphe + stats …")
    graph = build_graph(df)
    stats = compute_embeddings(df)

    print(f"[{lang_label}] Sauvegarde -> {out_graph}, {out_stats}")
    with open(out_graph, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    with open(out_stats, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

def main():
    print("=== Lancement de l'analyse Tarot (FR/EN) ===")

    # FR
    process_language("FR", DATA_FR, GRAPH_FR, STATS_FR, WC_FR)

    # EN
    process_language("EN", DATA_EN, GRAPH_EN, STATS_EN, WC_EN)

    # Manifest récapitulatif (pratique pour l’app)
    manifest = {
        "fr": {
            "graph": str(GRAPH_FR.relative_to(ROOT)),
            "stats": str(STATS_FR.relative_to(ROOT)),
            "wordcloud": str(WC_FR.relative_to(ROOT)),
        },
        "en": {
            "graph": str(GRAPH_EN.relative_to(ROOT)),
            "stats": str(STATS_EN.relative_to(ROOT)),
            "wordcloud": str(WC_EN.relative_to(ROOT)),
        },
    }
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("✅ Analyse terminée.")
    print("Manifest :", MANIFEST)

if __name__ == "__main__":
    main()
