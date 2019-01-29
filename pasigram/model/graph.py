import pandas as pd
from pasigram.model.edges import *
from pasigram.model.nodes import *
from pasigram.model.adjacency_list import *
from pasigram.model.adjacency_matrix import *
from pasigram.model.clusters import *
from pasigram.service.graph_service import *


class Graph:
    """A class to represent a directed graph with labels for the edges and nodes.

    ...

    Attributes
    ----------
        nodes : pd.DataFrame
            The nodes of the graph (id, label)
        nodes_ids : list
            List of all ids of the nodes
        edges : pd.DataFrame
            The edges of the graph (id, source, target)
        edges_ids : list
            List of all ids of the edges
        adjacency_matrix : pd.DataFrame
            Adjacency matrix of the graph (ids of nodes and edges)
        adjacency_list : pd.DataFrame
            Adjacency list of the graph
        node_degrees : pd.DataFrame
            Degrees of all nodes
        clusters_by_label_and_degree : pd.DataFrame
            Different clusters of nodes based on their labels, in-/outgoing degrees
        clusters_by_adjacency_list : pd.DataFrame
               Different clusters of nodes based on their labels, in-/outgoing degrees and adjacency lists
        canonical_code : String
            The canonical code of the graph

    """

    def __init__(self, nodes: pd.DataFrame, edges: pd.DataFrame) -> object:
        """

        Parameters
        ----------
        nodes : DataFrame
            Contains all nodes of the graph.
        edges : DataFrame
            Contains all edges of the graph.

        Returns
        -------
        object
        """
        # edges of the graph (pd.DataFrame)
        self.__edges = Edges(edges)

        # nodes of the graph (pd.DataFrame)
        self.__nodes = Nodes(nodes, self.edges)

        # adjacency matrix of the graph (pd.DataFrame)
        self.__adjacency_matrix = AdjacencyMatrix(self.__nodes.ids, self.__edges.ids, self.__edges.edges)

        # adjacency list of the graph (pd.DataFrame)
        self.__adjacency_list = AdjacencyList(self.__nodes.ids, self.__edges.edges, self.__nodes.nodes,
                                              self.__nodes.degrees)

        # initial clusters: nodes clustered by label and degrees (pd.DataFrame)
        self.__clusters = Clusters(self.nodes, self.node_degrees, self.adjacency_list)

        # canonical code of the graph build based on the final clusters
        self.__canonical_code = build_canonical_smallest_code(self.clusters_by_adjacency_list)

    @property
    def adjacency_matrix(self) -> pd.DataFrame:
        return self.__adjacency_matrix.adjacency_matrix

    @property
    def nodes(self) -> pd.DataFrame:
        return self.__nodes.nodes

    @property
    def nodes_ids(self) -> pd.DataFrame:
        return self.__nodes.ids

    @property
    def edges(self) -> pd.DataFrame:
        return self.__edges.edges

    @property
    def edges_ids(self) -> pd.DataFrame:
        return self.__edges.ids

    @property
    def adjacency_list(self) -> pd.DataFrame:
        return self.__adjacency_list.adjacency_list

    @property
    def node_degrees(self) -> pd.DataFrame:
        return self.__nodes.degrees

    @property
    def clusters_by_label_and_degree(self) -> pd.DataFrame:
        return self.__clusters.clusters_by_label_and_degree

    @property
    def clusters_by_adjacency_list(self) -> pd.DataFrame:
        return self.__clusters.clusters_by_adjacency_list

    @property
    def canonical_code(self) -> str:
        return self.__canonical_code