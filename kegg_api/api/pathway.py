import re
import matplotlib.pyplot as plt
import networkx as nx
from dataclasses import dataclass, field
from tqdm import tqdm

from kegg_api.api import KeggAPI
from kegg_api.utils.shapes import Rectangle, Circle, Line
from kegg_api.utils.extract import extract_ko, extract_reaction, extract_compound
from kegg_api.api.base_features import Reaction


def get_ko_from_pathway(pathway) -> list[str]:
    """
    :param pathway: str
    :return: dict
    """
    response: str = KeggAPI().link('ko', pathway).text
    return extract_ko(response)


def get_rection_from_pathway(pathway) -> list[str]:
    """
    :param pathway: str
    :return: dict
    """
    response: str = KeggAPI().link('reaction', pathway).text
    return extract_reaction(response)


def get_compound_from_pathway(pathway) -> list[str]:
    """
    :param pathway: str
    :return: dict
    """
    response: str = KeggAPI().link('compound', pathway).text
    return extract_compound(response)


@dataclass(init=True, repr=True)
class KeggPathwayGraph(object):
    pathway: str
    ko: list[str] = field(default_factory=list)
    reaction: list[str] = field(default_factory=list)
    compound: list[str] = field(default_factory=list)
    graph: nx.MultiGraph = field(default_factory=nx.MultiGraph)
    config: str = field(default=None)

    def __post_init__(self):
        self.ko = get_ko_from_pathway(self.pathway)
        self.reaction = get_rection_from_pathway(self.pathway)
        self.compound = get_compound_from_pathway(self.pathway)
        self.config = self.get_pathway_config()
        self.graph = nx.DiGraph()

    def get_pathway_config(self) -> str:
        return KeggAPI().get('pathway', self.pathway, 'conf').text

    def plot_graph(self,
                   ax: plt.axes = None,
                   add_ko_nodes: bool = False) -> nx.MultiGraph:
        if ax is None:
            f, ax = plt.subplots(figsize=(20, 20))
        self.update_nodes(add_ko_nodes=add_ko_nodes)
        self.update_edges(add_ko_edges=add_ko_nodes)
        node_size = nx.degree(self.graph)
        pos = nx.spring_layout(self.graph, k=0.5, iterations=50)
        if add_ko_nodes:
            nx.draw_networkx_nodes(self.graph,
                                   pos,
                                   nodelist=self.ko,
                                   node_size=[(node_size[node] + 1) * 30 for node in self.ko],
                                   node_color='green',
                                   edgecolors='black',
                                   ax=ax)
        nx.draw_networkx_nodes(self.graph,
                               pos,
                               nodelist=self.reaction,
                               node_size=[(node_size[node] + 1) * 30 for node in self.reaction],
                               node_color='blue',
                               edgecolors='black',
                               ax=ax)
        nx.draw_networkx_nodes(self.graph,
                               pos,
                               nodelist=self.compound,
                               node_size=[(node_size[node] + 1) * 30 for node in self.compound],
                               node_color='red',
                               edgecolors='black',
                               ax=ax)
        nx.draw_networkx_edges(self.graph,
                               pos,
                               edge_color='k')
        nx.draw_networkx_labels(self.graph,
                                pos,
                                font_size=8,
                                font_family='sans-serif',
                                ax=ax)
        plt.show()
        return self.graph

    def update_nodes(self, add_ko_nodes: bool = False) -> None:
        nodes = []
        for i in [self.ko if add_ko_nodes else None,
                  self.reaction,
                  self.compound]:
            if i is not None:
                nodes.extend(i)
        self.graph.add_nodes_from(nodes)

    def update_edges(self, add_ko_edges: bool) -> None:
        if add_ko_edges:
            # KO Edges
            ko_edges = self.__get_edges('reaction', self.ko, self.reaction)
            ko_edges = [[(i, j), (j,i)] for i, j in ko_edges]
            ko_edges = [i for j in ko_edges for i in j]
        else:
            ko_edges = []
        # Reaction Edges
        reaction_edges = [Reaction(i).generate_edges() for i in tqdm(self.reaction, total=len(self.reaction))]
        reaction_edges = [i for j in reaction_edges for i in j]
        self.graph.add_edges_from([*ko_edges, *reaction_edges])

    @staticmethod
    def __filter_feature_links(features: list[str],
                               links: list[list[str, str]]) -> list[tuple[str, str]]:
        links = [i for i in links if i]
        return [(i, j) for i, j in links if j in features]

    def __get_edges(self, __feature, __value: list[str], __filter_value) -> list[tuple[str, str]]:
        url_extension = '+'.join(__value)
        response = KeggAPI().link(__feature, url_extension).text
        edges = [re.findall(r'[K,R,C]\d{5}', i) for i in response.split('\n')]
        return self.__filter_feature_links(__filter_value, edges)