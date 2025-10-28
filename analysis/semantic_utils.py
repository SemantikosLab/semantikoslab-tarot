import networkx as nx
import numpy as np

def build_graph(df):
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_node(row["card"], meaning=row["description"])
    # exemple simplifié : relier par cooccurrence de mots
    for i, r1 in df.iterrows():
        for j, r2 in df.iterrows():
            if i < j and len(set(r1["description"].split()) & set(r2["description"].split())) > 2:
                G.add_edge(r1["card"], r2["card"])
    return nx.node_link_data(G)

def compute_embeddings(df):
    return {
        "num_cards": len(df),
        "avg_length": np.mean(df["description"].str.len())
    }

