import streamlit as st
import requests
import time
from treelib import Tree
import graphviz
url = "http://127.0.0.1:5000/"


st.title("BabbageCoin Blockchain")
imageLocation = st.empty()


def display_blockchain():
    resp = requests.get(f"{url}blocks/hashdict",
                             headers={"Content-Type": "application/json"},)

    hash_dict = resp.json()
    build_blockchain_tree(hash_dict)
    #st.json(hash_dict)
    graph = graphviz.Source.from_file('plot/tree_graph.dot')
    imageLocation.image(graph.render(format='jpg'))
    #st.image(graph.render(format='jpg'))

#    st.graphviz_chart(graph)
#    with open("plot/tree_graph.dot", "r") as f:
#        print("\n\n\n")
#        print(f.read())


def build_blockchain_tree(hash_dict):
    tree = Tree()
    #for hash, b in hash_dict.items():
    #    if hash == "":
    #        tree.create_node(tag=hash, identifier=hash, parent=None)
    #    else:
    #        tree.create_node(tag=hash, identifier=hash, parent=b["prev_hash"])
    #tree.to_graphviz(filename="plot/tree_graph.dot")
    b = hash_dict[""]
    tree.create_node(tag="THE GENESIS", identifier="", parent=None)
    add_next_blocks(b, tree)
    tree.to_graphviz(filename="plot/tree_graph.dot")

def add_next_blocks(b, tree):
    for child in b["next_blocks"]:
        tree.create_node(tag=child["hash"][-8:],
                         identifier=child["hash"],
                         parent=child["block"]["prev_hash"])
        add_next_blocks(child["block"], tree)


while True:
    display_blockchain()
    time.sleep(3)  # TODO: update when clicking on a button
