import pandas as pd
import time
from collections import deque


class Graph:
    # Graph structure to handle players and teammates
    def __init__(self):
        self.adjacency_list = {}

    def add_edge(self, player1, player2, weight=1):
        # Add an edge between two players who are teammates in a given year
        if player1 not in self.adjacency_list:
            self.adjacency_list[player1] = []
        if player2 not in self.adjacency_list:
            self.adjacency_list[player2] = []
        self.adjacency_list[player1].append((player2, weight))
        self.adjacency_list[player2].append((player1, weight))

def load_data(file_path):
    # Load the roster data from the CSV
    rosters = pd.read_csv(file_path)
    print("Data Loaded")
    print(rosters.head())
    print(rosters.info())
    return rosters
