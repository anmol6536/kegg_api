# KeggPath

---

## Description
This is a python package for working with KEGG pathways. It is designed to be used with the [KEGG REST API](https://www.kegg.jp/kegg/rest/keggapi.html).
KeggPath generates and returns a networkx graph object from a KEGG pathway map. This allows for easy integration with other python packages and algorithms that work with networkx graphs.
Reactions and compounds are represented as nodes in the graph, and edges represent the relationship between them. Flow of information is represented by directed edges.
Kegg Orthology IDs (KO IDs) which represent genes or enzymes are also included as node relations. This allows for easy integration with other KEGG REST API functions.
Depending on the usecase KOs can be represented as nodes or attributes of nodes.

## Installation

```bash
pip install git+https://github.com/anmol6536/kegg_api.git
```

---

## Usage

```python
# IMPORTS
from kegg.api.pathway import KeggPathwayGraph

# INSTANTIATE
pathway = KeggPathwayGraph("map00220")

# GET GRAPH W/ KOs AS NODES
pathway.plot_graph(add_ko_nodes=True)

# GET GRAPH W/O KOs
pathway.plot_graph(add_ko_nodes=False)
 ```
---

> Example Notebook:  
