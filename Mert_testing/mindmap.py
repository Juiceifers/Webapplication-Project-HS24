import networkx as nx
import matplotlib.pyplot as plt
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

TOKENIZER = BertTokenizer.from_pretrained("bert-base-uncased")
MODEL = BertModel.from_pretrained("bert-base-uncased")

def get_embeddings(text):
    input_ids = TOKENIZER.encode(text, return_tensors="pt", truncation=True, padding=True)
    
    with torch.no_grad():
        output = MODEL(input_ids)
        
    embeddings = output.last_hidden_state.mean(dim=1)
    
    return embeddings

def create_mindmap(text):
    lines = text.splitlines()
    graph = nx.DiGraph()
    nodes = []
    embeddings = []

    # Extract nodes and their embeddings
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            nodes.append(stripped_line)
            graph.add_node(stripped_line)
            emb = get_embeddings(stripped_line)
            embeddings.append(emb.detach().numpy().flatten())  # Flatten the tensor for clustering

    # Cluster nodes based on embeddings
    kmeans = KMeans(n_clusters=5)  # Adjust the number of clusters based on specific data
    labels = kmeans.fit_predict(embeddings)

    # Connect nodes within the same cluster if their similarity is high
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if labels[i] == labels[j]:  # Only connect nodes if they are in the same cluster
                emb1 = get_embeddings(nodes[i])
                emb2 = get_embeddings(nodes[j])
                similarity = cosine_similarity(emb1.numpy(), emb2.numpy())[0][0]
                if similarity > 0.8:  # Threshold for connecting nodes, can be adjusted
                    graph.add_edge(nodes[i], nodes[j])

    return graph

def visualize_mindmap(graph):
    pos = nx.kamada_kawai_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold")
    plt.show()

if __name__ == "__main__":

    # Example input
    text_input = """
    Root
        Machine Learning
            Supervised Learning
            Unsupervised Learning
        Tree
            Birch
            Oak
            Pine
        Artificial Intelligence
            Natural Language Processing
            Computer Vision
        Cars
            BMW
            Mercedes-Benz
            Audi
    """

    graph = create_mindmap(text_input)
    visualize_mindmap(graph)