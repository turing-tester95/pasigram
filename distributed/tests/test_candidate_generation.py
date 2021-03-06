from unittest import TestCase
import pandas as pd
from pasigram.controller.candidate_generation.utils \
    import compute_right_most_path_nodes, add_new_forward_edge, compute_relevant_forward_edges, \
    compute_relevant_backward_edges
from pasigram.model.graph import Graph


class TestRightMostPath(TestCase):

    def test_compute_right_most_path_nodes(self):
        expected = sorted([1, 0, 2])
        edges = pd.DataFrame.from_dict({0: [0, 1, "a"],
                                        1: [1, 0, "b"],
                                        2: [1, 2, "a"]}, orient='index',
                                       columns=['source', 'target', 'label'])

        right_most_path = [0, 1, 2]
        right_most_path_nodes = sorted(compute_right_most_path_nodes(right_most_path, edges))
        print(right_most_path_nodes)
        self.assertEqual(expected, right_most_path_nodes, msg="Test for the matrix")

    def test_compute_relevant_edges(self):
        expected_result = pd.DataFrame.from_dict({'DBDMa': ['DB', 'DM', 'a', int(2)],
                                                  'DBIRb': ['DB', 'IR', 'b', int(3)], }, orient='index',
                                                 columns=['source', 'target', 'label', 'frequency'])
        frequent_edges = pd.DataFrame.from_dict({'DBDMa': ['DB', 'DM', 'a', int(2)],
                                                 'DBIRb': ['DB', 'IR', 'b', int(3)],
                                                 'IRDMc': ['IR', 'DM', 'c', int(2)],
                                                 'IRIRe': ['IR', 'IR', 'e']}, orient='index',
                                                columns=['source', 'target', 'label', 'frequency'])
        current_node_label = 'DB'

        relevant_edges = compute_relevant_forward_edges(current_node_label, frequent_edges)

        self.assertEqual(expected_result.values.tolist(), relevant_edges.values.tolist(),
                         msg="Test for the relevant forward edges")

    def test_add_new_forward_edge(self):
        edges = pd.DataFrame.from_dict({0: [0, 1, "b"]}, orient='index', columns=['source', 'target', 'label'])
        nodes = pd.DataFrame.from_dict({0: ["DB"],
                                        1: ["IR"]}, orient='index', columns=['label'])

        graph = Graph(nodes, edges)

        graph.root_node = 0

        new_edge = pd.Series(data=['DB', 'DM', 'a'], index=['source', 'target', 'label'])

        new_graph = add_new_forward_edge(graph, new_edge, 0)

        print(new_graph.edges)
        print(new_graph.nodes)
        print(new_graph.csp_graph)

    def test_compute_relevant_backward_edges(self):
        edges = pd.DataFrame.from_dict({0: [0, 1, "a"],
                                        1: [1, 0, "a"]}, orient='index', columns=['source', 'target', 'label'])
        nodes = pd.DataFrame.from_dict({0: ["IR"],
                                        1: ["IR"]}, orient='index', columns=['label'])

        graph = Graph(nodes, edges)
        graph.root_node = 0
        graph.right_most_node = 1
        graph.right_most_path = [0, 1]

        relevant_backward_edges = compute_relevant_backward_edges(graph.right_most_node, graph.right_most_path,
                                                                  graph.edges).values

        expected = pd.DataFrame.from_dict({0: [1, 0, "a"],
                                           1: [0, 1, "a"]}, orient='index',
                                          columns=['source', 'target', 'label']).values
        print(relevant_backward_edges)

        self.assertEqual(relevant_backward_edges.tolist(), expected.tolist(),
                         msg="Test for the relevant backward edges of a node")
