import networkx as nx
import pandas as pd
import re
import numpy as np


class Graph(object):
    def __init__(self, df_hero_net=None, df_edges=None, df_nodes=None):
        try:
            self.df_hero_net = pd.read_csv(df_hero_net)
        except:
            pass
        try:
            self.df_nodes = pd.read_csv(df_nodes)
        except:
            pass

        try:
            self.df_edges = pd.read_csv(df_edges)
        except:
            pass
        self.G_2 = nx.Graph()
        self.G_1 = nx.Graph()

    def create_graph_edges_nodes(self):

        self.G_2.add_nodes_from(self.df_nodes.loc[self.df_nodes.type == 'hero'].node, size='H')
        self.G_2.add_nodes_from(self.df_nodes.loc[self.df_nodes.type == 'comic'].node, size='C')
        self.G_2.add_edges_from(self.df_edges.to_numpy())
        return self.G_2

    def number_nodes(self):
        return self.G_2.number_of_edges()

    def get_Dataframe(self):
        df_between = pd.DataFrame.from_dict(nx.degree_centrality(self.G),
                                            orient='index',
                                            columns=['betweenness']).sort_values(by='betweenness', ascending=False)
        return df_between

        # node_df = pd.DataFrame({attr: G.vs[attr] for attr in G.vertex_attributes()})
        # edge_df = pd.DataFrame({attr: G.es[attr] for attr in G.edge_attributes()})


class Preprocessing:

    def __init__(self):
        self.df_wrong = pd.read_csv('hero-network.csv')  # wrong dataset
        self.df_right = pd.read_csv('edges.csv')  # right dataset
        self.df_nodes = pd.read_csv('nodes.csv')
        self.dic = {}

    def get_names(self):
        # Extract all the names from the edges
        vec_right = self.df_right.hero.unique()
        clean_right = set(map(Preprocessing.cleaning, vec_right))

        # Extract all the names of the heroes that might be wrong (col hero1)
        vec_wrong_hero_1 = self.df_wrong.hero1.unique()
        new_vec_wrong_hero_1 = set(map(Preprocessing.cleaning, vec_wrong_hero_1))

        # Extract all the names of the heroes that might be wrong (col hero2)
        vec_wrong_hero_2 = self.df_wrong.hero2.unique()
        new_vec_wrong_hero_2 = set(map(Preprocessing.cleaning, vec_wrong_hero_2))

        # Merge
        merge_hero_wrong = new_vec_wrong_hero_1.union(new_vec_wrong_hero_2)

        self.dic = {}
        # Iterate over the wrong hero names
        for x in merge_hero_wrong:

            # Iterate over the right hero names
            for y in clean_right:
                self.dic[x] = x
                if x in y:
                    self.dic[x] = y
                    break
        return self.dic

    def cleaning_dataset(self):
        # Clean the values in both columns
        self.df_wrong.hero1 = self.df_wrong.hero1.apply(lambda row: Preprocessing.cleaning(row))
        self.df_wrong.hero2 = self.df_wrong.hero2.apply(lambda row: Preprocessing.cleaning(row))

        # Replace the wrong names with the right ones
        self.dic = Preprocessing().get_names()
        self.df_wrong["hero1"] = self.df_wrong.hero1.apply(lambda row: self.dic[row])
        self.df_wrong["hero2"] = self.df_wrong.hero2.apply(lambda row: self.dic[row])

        # Clean the values in nodes.node
        self.df_nodes.node = self.df_nodes.node.apply(lambda row: Preprocessing.cleaning(row))
        self.df_nodes.node.loc[self.df_nodes.node == 'SPIDER-MAN/PETER PARKERKER'] = 'SPIDER-MAN/PETER PARKER'

        # remove duplicates rows from hero network
        self.df_wrong = self.df_wrong[self.df_wrong.hero1 != self.df_wrong.hero2]

        return self.df_wrong, self.df_right, self.df_nodes

    @staticmethod
    def cleaning(string):
        # Pattern for backslash in last position
        pattern = "\/$"
        new_string = re.sub(pattern, "", string)
        # pattern for space in last position
        pattern = " $"
        new_string = re.sub(pattern, "", new_string)

        return new_string
