
import fitz
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import rcParams
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP
import pandas as pd
from transformers.pipelines import pipeline
import spacy
import re
import flask
from flask import Flask

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from Mert_testing.summarizer import get_summarized_pdf, get_summarized_text
from Mert_testing.new_summarizer import summarize_pdf, new_summarize_text

spacy

spacy.prefer_gpu()


def text_iter_from_pdf(pdf_path, split_lines=False):
    text = []

    spans = []

    it = [pdf_path] if isinstance(pdf_path, str) else pdf_path

    for pdf_path in it:
        doc = fitz.open(pdf_path)
        for i, page in enumerate(doc):

            doc_path = pdf_path.split("/")[-1] + f" /page_{i}"

            #for html_text in page.get_text("html"):
                #block_text = re.findall(r"<div.*<\/div>", page.get_text("html"))
                #text.append(page.get_text("html"))

            #for (x0, y0, x1, y1, block_text, block_no, block_type) in page.get_text("blocks"):

            blocks = [x[4] for x in page.get_text("blocks")]

            if len(blocks) > 2:

                join_flag = any([len(block_text.split(" ")) < 5 for block_text in blocks])

                if join_flag:
                    text.append(page.get_text())
                    spans.append(doc_path)
                else:
                    for block_text in blocks:
                        if split_lines:
                            text += block_text.split("\n")
                        elif len(block_text.split(" ")) > 2:
                            text.append(block_text)
                            spans.append(doc_path)



                #for block_text in page.get_text("blocks"):                

            else:
                text.append(page.get_text())
                spans.append(doc_path)


            #text += f"<PAGE {i}>\n{page.get_text().strip().replace("\n", "\n\t")}\n<PAGE END>\n"

    return text, spans

def try_bert(text, spans, map_name="DEFAULT_MAP"):

    pd.set_option('display.max_columns', None)

    #embedding_model = spacy.load("en_core_web_trf", exclude=['tagger', 'parser', 'ner', 
    #                                         'attribute_ruler', 'lemmatizer'])
    embedding_model = pipeline("feature-extraction", model="distilbert-base-cased")

    umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state=42)
    vectorizer_model = CountVectorizer(stop_words="english")

    representation_model = KeyBERTInspired()
    #topic_model = BERTopic()
    topic_model = BERTopic(n_gram_range=(1, 2), min_topic_size=4, embedding_model=embedding_model,umap_model=umap_model,calculate_probabilities=False, vectorizer_model=vectorizer_model, representation_model=representation_model)

    print("text doc count:", len(text))
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

    #print(topic_model.get_topic_info())
    #print(topic_model.custom_labels_)

    #terms = topic_model.visualize_barchart()
    #terms.show()
    #.write_html("bertopic/hierarchy.html")

    print(text)

    print("Topics::")
    for k,v in topic_model.get_topics().items():
        print(f"Topic Index {k}, label:{topic_model.custom_labels_[k]}")
        pout = ""
        for i in v:
            pout += f"{i[0]}; "
        
        print(pout)

    print(f"TOPICS:{len(topic_model.get_topics())}; TEXTS:{len(text)}")

    hierarchical_topics = topic_model.hierarchical_topics(text)

    #topic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics, custom_labels=True)
    #
    #fig = topic_model.visualize_hierarchy(custom_labels=True)
    #fig.show()
    #fig.write_html("data/hierarchy.html")
    #hierarchical_topics.to_csv("data/hierarchy_df.csv")



    tree = topic_model.get_topic_tree(hierarchical_topics)
    #print(tree)

    topic_distr, _ = topic_model.approximate_distribution(text, calculate_tokens=True)

    print(topic_distr.shape)
#    topic_model.visualize_distribution(topic_distr[0])

    #for i in range(topic_distr.shape[0]):
    #    print(topic_distr[i])

    print("DOCUMENT INFO")
    document_info = topic_model.get_document_info(text)
    print(document_info)

    #print("Hierarchy:")
    #for t in hierarchical_topics:
    #    print(t)

    render_text = render_as_html(topic_model, text, spans, tree)

    return render_text

    
    #with open(f"maps/MAP_{map_name}.html", "w", encoding="utf-8") as txt_map_file:
#
    #    if __name__ == "__main__":
    #        app = Flask(__name__)
#
    #        render_text = render_as_html(topic_model, text, spans, tree)
#
    #        with app.app_context():
    #            txt_map_file.write(render_text)
    #    else:
    #        txt_map_file.write(render_text)
#
    #return render_text



    print(hierarchical_topics.head())

    #G = create_networkx_tree(hierarchical_topics)
    #visualize_networkx_tree(G)


    #visualize_mindmap(tree)
    #tree = create_tree_structure(hierarchical_topics)
    #print(topic_model.topic_labels_)

def load_df():
    hierarchical_topics = pd.read_csv("data/hierarchy_df.csv")

    visualize_topic_tree(hierarchical_topics)


def render_as_html(topic_model, text, spans, tree):


    print("starting summary...")
    summz = []

    for fil in FILES_CACHE:
        summz.append((fil.split("/")[-1], summarize_pdf(fil)))
        
    #print(summz)
                


    ctx = {}
    print(tree)
    ctx["tree"] = tree.replace("\t", "&emsp;")
    tree_iter = tree.replace("    ", "&emsp;").split("\n")
    #tree_iter = tree.replace("\t", "&emsp;").split("\n")

    print(tree_iter)

    df = topic_model.get_document_info(text)

    #for doc_info in df.iterrows():


    paragraphs = []

    topic_paras = []

    for topic_index in range(len(topic_model.topics_)):

        cur_topic_docs = []

        for i in range(len(df)):
            #if i < 1:
            #    continue

            #if df["Representative_document"][i]:

            if df["Topic"][i] != topic_index:
                continue

            doc_file = spans[i]

            title = f"{doc_file}, doc-id {i}"
            topic_title = f"TOPIC {topic_index}: \t{df["CustomName"][i]}"
            val = df["Document"][i].split("\n")
            #txt_map_file.write(f"<div><h1>{title}</h1>\n\t<p>{val}</p>\n</div>\n")

            paragraphs.append((title,topic_title,val))

            cur_topic_docs.append((title, i, val))

        if len(cur_topic_docs) > 0:
            topic_paras.append([topic_title, topic_index, cur_topic_docs])


    

    topic_texts = [[t[0], t[1], " ".join(list(  map( lambda x: " ".join(x[2]),  t[2] )))] for t in topic_paras]
    topic_texts = [new_summarize_text(text[2]) for text in topic_texts]

    for t in range(len(topic_paras)):
        topic_paras[t].append(topic_texts[t])

    

    #topic_texts = [[t[0], t[1], " ".join(list(  map( lambda x: " ".join(x[2]),  t[2] )))] for t in topic_paras for s in topic_texts]

    ctx["paragraphs"] = paragraphs

    source = """
    <html>
    <head>
    </head>
    <body>
      <div>
          <h2>Tree:</h2>
            <p>
            {% autoescape false %}
                {% for t in tree_iter %}
                    {{ t }}<br>
                {% endfor %}
            {% endautoescape %}
            </p>
      </div>

      <div>
        <h2>Index:</h2>

        <h3>Summaries</h3>
        {% for ftitle, summ in summaries %}
            <a href="#sum_{{  ftitle  }}">{{  ftitle  }} summary</a><br>
        {% endfor %}

        <br>

        <h3>Topics and Docs</h3>
        {% for topic_title, topic_index, paragraphs, topic_summ in topic_paras %}
        <a href="#t_{{  topic_index  }}">{{  topic_title  }}</a><br>
            {% for title, par_index, val in paragraphs %}
                &emsp;<a href="#d_{{  par_index  }}">{{  title  }}</a><br>
            {% endfor %}
        {% endfor %}

      </div>

      <div>
        <h2>Summaries:</h2>
        {% for ftitle, summ in summaries %}
            <h3 id="sum_{{  ftitle  }}">{{  ftitle  }}</h3><br>
                <p>{{  summ  }}</p>
            <br>
        {% endfor %}
      </div>

      <div>
      {% for topic_title, topic_index, paragraphs, topic_summ in topic_paras %}
        <div>
        <h2 id="t_{{  topic_index  }}">{{ topic_title }}</h2>
            <p>{{  topic_summ  }}</p>
            {% for title, par_index, val in paragraphs %}
                <div>
                    <h3 id="d_{{  par_index  }}">{{ title }}</h3>
                    <p style="margin:10px">
                        {% for i in val %}
                            {{ i }}<br>
                        {% endfor %}
                    </p>
                </div>
            {% endfor %}
        </div>
    {% endfor %}
    </div>
    </body>
    </html>
    """


    output = flask.render_template_string(source, summaries=summz, tree_iter=tree_iter,topic_paras=topic_paras, tree=tree)

    return output


import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def create_networkx_tree(hierarchical_topics_df, custom_labels=None):
    """
    Create a NetworkX tree graph from hierarchical_topics data.

    Parameters:
        hierarchical_topics_df (pd.DataFrame): DataFrame with columns:
                                               Parent_ID, Child_Left_ID, Child_Right_ID.
        custom_labels (dict): Mapping of topic IDs to custom labels.

    Returns:
        G (networkx.DiGraph): Directed graph representing the hierarchical tree.
    """
    G = nx.DiGraph()
    
    # Iterate through rows and add parent-child relationships
    for _, row in hierarchical_topics_df.iterrows():
        parent_id = row['Parent_ID']
        child_left_id = row['Child_Left_ID']
        child_right_id = row['Child_Right_ID']
        
        # Use custom labels if available
        parent_label = custom_labels.get(parent_id, row['Parent_Name']) if custom_labels else row['Parent_Name']
        child_left_label = custom_labels.get(child_left_id, row['Child_Left_Name']) if custom_labels else row['Child_Left_Name']
        child_right_label = custom_labels.get(child_right_id, row['Child_Right_Name']) if custom_labels else row['Child_Right_Name']
        
        # Add edges to the graph
        G.add_edge(parent_label, child_left_label)
        G.add_edge(parent_label, child_right_label)
    
    return G

def visualize_networkx_tree(G, figsize=(12, 8), title="Topic Hierarchy"):
    """
    Visualize a tree structure using NetworkX.

    Parameters:
        G (networkx.DiGraph): Directed graph representing the hierarchical tree.
        figsize (tuple): Size of the figure.
        title (str): Title for the visualization.
    """

    rcParams['font.family'] = 'DejaVu Sans'

    try:
        # Use graphviz layout for a tree structure
        #pos = nx.drawing.nx_agraph.graphviz_layout(G, prog="dot")
        
        #pos = nx.drawing.nx_pydot.pydot_layout(G, prog="dot")
        
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=5, iterations=100)  # Tree layout


    except ImportError:
        raise ImportError("Graphviz layout requires 'pygraphviz' or 'pydot'. Install one of them to use this function.")
    

    plt.figure(figsize=figsize)
    nx.draw(
        G, 
        pos, 
        with_labels=True, 
        node_color="lightblue", 
        node_size=2000,
        font_size=10, 
        font_weight="bold", 
        arrows=True
    )
    plt.title(title)
    plt.show()


def visualize_topic_tree(hierarchical_topics, title="Topic Hierarchy"):
    """
    Visualizes the topic tree as a directed graph.
    """

    roots = []
    for i in hierarchical_topics["Parent_ID"]:
        print(i)

    topic_tree = nx.DiGraph()
    topic_tree = nx.tree.tree_graph

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

FILES_CACHE = []

def process_file(file_path):

    global FILES_CACHE

    FILES_CACHE = [file_path] if isinstance(file_path, str) else file_path

    txt, spans = text_iter_from_pdf(file_path, split_lines=False)
    
    
    return try_bert(txt, spans)



if __name__ == "__main__":

    import sys  
    encoding = sys.getdefaultencoding()  
    print("DEFAULT ENCODING:",encoding)  
    

#    create_txt(filepath)
    filepath = "bertopic/lecture1-introduction.pdf"
    filepath = "uploads/callaway.pdf"
    filepath = "uploads/MAT-notes-part1.pdf"

    filepath = [
        "uploads/pcl2/1_Introduction.pdf",
        "uploads/pcl2/2_Test_Driven_Development.pdf",
        "uploads/pcl2/03_Object_Oriented_Programming.pdf",
        "uploads/pcl2/04_Structuring_Python_Projects_slides.pdf",
        "uploads/pcl2/05_Functional_Programming.pdf",
        "uploads/pcl2/06_Computational_Complexity_slides.pdf",
        "uploads/pcl2/07_Namespaces_References.pdf",
        "uploads/pcl2/08_Text_Encoding_slides.pdf",
        "uploads/pcl2/09_Numerical_Data_Processing.pdf",
        "uploads/pcl2/10_Data_Scaling.pdf",
        "uploads/pcl2/11_Code_Optimization.pdf",
        "uploads/pcl2/12_Multimodal_Data_Processing_slides.pdf",
        "uploads/pcl2/Tutorial_01.pdf",
        "uploads/pcl2/Tutorial_03.pdf",
        "uploads/pcl2/Tutorial_04.pdf",
        "uploads/pcl2/Tutorial_05.pdf",
        "uploads/pcl2/Tutorial_06.pdf",
        "uploads/pcl2/Tutorial_07.pdf",
        "uploads/pcl2/Tutorial_08.pdf",
        "uploads/pcl2/Tutorial_09.pdf",
    ]

    filepath = ["uploads/MAT-notes-part1.pdf", "uploads/MAT-notes-part2.pdf"]

    
    filepath = [
        "uploads/ltwa/2024-09-18.pdf",
        "uploads/ltwa/2024-09-25.pdf",
        "uploads/ltwa/2024-10-02.pdf",
        "uploads/ltwa/2024-10-09.pdf",
        "uploads/ltwa/2024-10-16.pdf",
        "uploads/ltwa/2024-10-23.pdf",
    ]


    process_file(filepath)
#    txt, spans = text_iter_from_pdf(filepath, split_lines=False)
#    try_bert(txt, spans)

    #hierarchical_topics = pd.read_csv("data/hierarchy_df.csv", encoding="utf-8")
    #G = create_networkx_tree(hierarchical_topics)
    #visualize_networkx_tree(G)


#    with open("bertopic/pdf_text.txt", encoding="UTF-8") as f:
#        try_bert(f.read())
