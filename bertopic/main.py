
import fitz
import networkx as nx
import matplotlib.pyplot as plt
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP
import pandas as pd
from transformers.pipelines import pipeline
import spacy

spacy

spacy.prefer_gpu()

#from bertopic import BERTopic
#from sklearn.datasets import fetch_20newsgroups

#docs = fetch_20newsgroups(subset='all',  remove=('headers', 'footers', 'quotes'))['data']

#topic_model = BERTopic()
#topics, probs = topic_model.fit_transform(docs)


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ''
    for i, page in enumerate(doc):
        text += page.get_text()
        #text += f"<PAGE {i}>\n{page.get_text().strip().replace("\n", "\n\t")}\n<PAGE END>\n"
    return text

def text_iter_from_pdf(pdf_path, split_lines=False):
    text = []

    it = [pdf_path] if isinstance(pdf_path, str) else pdf_path

    for pdf_path in it:
        doc = fitz.open(pdf_path)
        for i, page in enumerate(doc):

            if split_lines:
                text += page.get_text().split("\n")
            else:
                text.append(page.get_text())
            #text += f"<PAGE {i}>\n{page.get_text().strip().replace("\n", "\n\t")}\n<PAGE END>\n"
    return text


def try_bert(text):

    pd.set_option('display.max_columns', None)

    #embedding_model = spacy.load("en_core_web_trf", exclude=['tagger', 'parser', 'ner', 
    #                                         'attribute_ruler', 'lemmatizer'])
    embedding_model = pipeline("feature-extraction", model="distilbert-base-cased")

    umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state=42)
    vectorizer_model = CountVectorizer(stop_words="english")
    # Fine-tune your topic representations
    representation_model = KeyBERTInspired()
    #topic_model = BERTopic()
    topic_model = BERTopic(n_gram_range=(1, 2), embedding_model=embedding_model,umap_model=umap_model,calculate_probabilities=False, vectorizer_model=vectorizer_model, representation_model=representation_model)


    print("running BERTopic on pdf text...")
    topics, probs = topic_model.fit_transform(text)
    print("Fitting complete!")

    #print(f"topics:\n{topics}")
    #print(f"probs:\n{probs}")

    topic_labels = topic_model.generate_topic_labels(nr_words=3,
                                                 topic_prefix=False,
                                                 word_length=10,
                                                 separator=", ")
    topic_model.set_topic_labels(topic_labels)

    print(topic_model.get_topic_info())
    print(topic_model.custom_labels_)

    terms = topic_model.visualize_barchart()
    terms.show()
    #.write_html("bertopic/hierarchy.html")

    print("Topics::")
    for k,v in topic_model.get_topics().items():
        print(f"Topic Index {k}, label:{topic_model.custom_labels_[k]}")
        pout = ""
        for i in v:
            pout += f"{i[0]}; "
        
        print(pout)

    hierarchical_topics = topic_model.hierarchical_topics(text)
    topic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics)

    fig = topic_model.visualize_hierarchy()
    fig.show()
    fig.write_html("bertopic/hierarchy.html")

    hierarchical_topics.to_csv("bertopic/hierarchy_df.csv")

    tree = topic_model.get_topic_tree(hierarchical_topics)
    print(tree)

    topic_distr, _ = topic_model.approximate_distribution(text, calculate_tokens=True)

    print(topic_distr.shape)
#    topic_model.visualize_distribution(topic_distr[0])

    #for i in range(topic_distr.shape[0]):
    #    print(topic_distr[i])

    print("DOCUMENT INFO")
    document_info = topic_model.get_document_info(text)
    print(document_info)

    print("Hierarchy:")
    for t in hierarchical_topics:
        print(t)

    print(hierarchical_topics.head())

    visualize_topic_tree(hierarchical_topics)
    #visualize_mindmap(tree)
    #tree = create_tree_structure(hierarchical_topics)

    #print(topic_model.topic_labels_)

def load_df():
    hierarchical_topics = pd.read_csv("bertopic/hierarchy_df.csv")

    visualize_topic_tree(hierarchical_topics)



# Step 3: Visualize the tree as a graph
def visualize_topic_tree(hierarchical_topics, title="Topic Hierarchy"):
    """
    Visualizes the topic tree as a directed graph.
    """

    roots = []
    for i in hierarchical_topics["Parent_ID"]:
        print(i)

    topic_tree = nx.DiGraph()

    for _, row in hierarchical_topics.iterrows():
        parent_id = row["Parent_ID"]
        parent_name = row["Parent_Name"]
        child_left_id = row["Child_Left_ID"]
        child_left_name = row["Child_Left_Name"]
        child_right_id = row["Child_Right_ID"]
        child_right_name = row["Child_Right_Name"]

        # Add parent node
        topic_tree.add_node(parent_id, label=parent_name)

        # Add left child
        if not pd.isna(child_left_id):
            topic_tree.add_node(child_left_id, label=child_left_name)
            topic_tree.add_edge(parent_id, child_left_id)

        # Add right child
        if not pd.isna(child_right_id):
            topic_tree.add_node(child_right_id, label=child_right_name)
            topic_tree.add_edge(parent_id, child_right_id)

    pos = nx.spring_layout(topic_tree, seed=42)  # Spring layout for better visualization
    labels = nx.get_node_attributes(topic_tree, "label")

    plt.figure(figsize=(10, 8))
    nx.draw(
        topic_tree,
        pos,
        labels=labels,
        with_labels=True,
        node_size=3000,
        node_color="lightgreen",
        font_size=10,
        font_color="black",
        edge_color="gray",
    )
    plt.title(title, fontsize=16)
    plt.show()


def create_txt(filepath):
    text = extract_text_from_pdf(filepath)

    #print(text)

    with open("bertopic/pdf_text_clean.txt", "w", encoding="UTF-8") as f:
        f.write(text)
    return text


# Sample text data (replace with your extracted text)
documents = [
    "Artificial Intelligence is transforming technology and industries.",
    "Machine learning is a subset of Artificial Intelligence focusing on data.",
    "Deep learning, part of machine learning, uses neural networks for analysis.",
    "Natural Language Processing enables understanding of human language.",
    "Robotics combines AI and physical machines for automated tasks.",
    "Cybersecurity ensures systems and networks are protected."
]


def create_tree_structure(h_topics):
    """
    Recursively create a tree structure from BERTopic hierarchical topics.
    """
    tree = nx.DiGraph()
    def add_nodes_edges(parent, children):
        for child in children:
            if isinstance(child, tuple):  # If it's a branch
                parent_topic, child_topics = child
                tree.add_edge(parent, parent_topic)
                add_nodes_edges(parent_topic, child_topics)
            else:  # It's a leaf
                tree.add_edge(parent, child)

    root_topic, child_topics = h_topics['root']
    tree.add_node(root_topic)  # Root node
    add_nodes_edges(root_topic, child_topics)
    return tree




# Step 5: Visualize the tree as a mindmap
def visualize_mindmap(tree, title="Topic Mindmap"):
    """
    Visualizes the tree structure as a mindmap using NetworkX and Matplotlib.
    """
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(tree)  # Tree layout
    nx.draw(
        tree,
        pos,
        with_labels=True,
        node_size=3000,
        font_size=10,
        node_color="lightblue",
        font_color="black",
        edge_color="gray",
    )
    plt.title(title, fontsize=16)
    plt.show()

#visualize_mindmap(topic_tree)




if __name__ == "__main__":

    load_df()
    quit(0)

    filepath = "bertopic/MAT-notes-part1.pdf"
    filepath = ["bertopic/MAT-notes-part1.pdf", "bertopic/MAT-notes-part2.pdf"]
#    create_txt(filepath)
    filepath = "bertopic/lecture1-introduction.pdf"
    filepath = "bertopic/callaway.pdf"

    txt = text_iter_from_pdf(filepath, split_lines=True)

    #try_bert(txt)
    try_bert(txt)

#    with open("bertopic/pdf_text.txt", encoding="UTF-8") as f:
#        try_bert(f.read())
