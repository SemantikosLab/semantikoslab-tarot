import networkx as nx
import numpy as np

def build_graph(df):
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_node(row["name"], meaning=row["summary_text"])
    # exemple simplifié : relier par cooccurrence de mots
    for i, r1 in df.iterrows():
        for j, r2 in df.iterrows():
            if i < j and len(set(r1["summary_text"].split()) & set(r2["summary_text"].split())) > 2:
                G.add_edge(r1["name"], r2["name"])
    return nx.node_link_data(G)

def compute_embeddings(df):
    return {
        "num_cards": len(df),
        "avg_length": np.mean(df["summary_text"].str.len())
    }

