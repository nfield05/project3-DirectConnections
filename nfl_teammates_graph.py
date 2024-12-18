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

    def dijkstra_shortest_path(self, start, target):
        # Find the shortest path using Dijkstra's algorithm
        import heapq

        heap = [(0, start, [start])]
        visited = set()
        node_visits = 0  # Count visited nodes

        while heap:
            current_distance, current_node, path = heapq.heappop(heap)
            node_visits += 1

            if current_node == target:
                return path, node_visits

            if current_node not in visited:
                visited.add(current_node)

                for neighbor, weight in self.adjacency_list.get(current_node, []):
                    if neighbor not in visited:
                        heapq.heappush(heap, (current_distance + weight, neighbor, path + [neighbor]))

        return None, node_visits

    def bfs_shortest_path(self, start, target):
        # Find the shortest path using BFS
        queue = deque([(start, [start])])
        visited = set()
        node_visits = 0  # Count visited nodes

        while queue:
            current, path = queue.popleft()
            node_visits += 1

            if current == target:
                return path, node_visits

            if current not in visited:
                visited.add(current)
                for neighbor, _ in self.adjacency_list.get(current, []):
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))

        return None, node_visits

def load_data(file_path):
    # Load the roster data from the CSV
    rosters = pd.read_csv(file_path)
    print("Data Loaded")
    print(rosters.head())
    print(rosters.info())
    return rosters

def build_graph(rosters):
    # Build a graph where nodes are players and edges represent playing on the same team within the same year
    graph = Graph()

    # Group by season and team to find all players on the same team in the same season
    grouped = rosters.groupby(['season', 'team'])

    for (season, team), group in grouped:
        players = group['player_id'].tolist()

        for i, player1 in enumerate(players):
            for player2 in players[i + 1:]:
                graph.add_edge(player1, player2, weight=1)

    print("Graph built successfully")
    return graph

def get_path_data(path, rosters):
    # takes in shortest path and prints it
    for i in range(len(path) - 1):
        player1 = path[i]
        player2 = path[i + 1]

        # Find the common team and season for these two players
        player1_data = rosters[rosters['player_id'] == player1]
        player2_data = rosters[rosters['player_id'] == player2]

        commonTeam = pd.merge(player1_data, player2_data, on=['team', 'season'])
        if not commonTeam.empty:
            team = commonTeam.iloc[0]['team']
            year = commonTeam.iloc[0]['season']
            print(
                f"{player1_data.iloc[0]['player_name']} played with "
                f"{player2_data.iloc[0]['player_name']} on the {year} {team}."
            )
        else:
            print(f"No direct shared team/season data for {player1} and {player2}.")

def compare_algorithms(graph, rosters):
    # Compare BFS and Dijkstra's shortest path algorithms with metrics
    try:
        source = input("Enter the source player ID for shortest path: ")
        target = input("Enter the target player ID for shortest path: ")

        # BFS
        start_time = time.time()
        bfs_path, bfs_visited_nodes = graph.bfs_shortest_path(source, target)
        bfs_time = time.time() - start_time
        print("\nBFS Metrics:")
        if bfs_path:
            print(f"Path Length: {len(bfs_path) - 1}")
            print(f"Visited Nodes: {bfs_visited_nodes}")
            print(f"Execution Time: {bfs_time:.6f} seconds")
            get_path_data(bfs_path, rosters)
        else:
            print("No path found using BFS.")

        # Dijkstra
        start_time = time.time()
        dijkstra_path, dijkstra_visited_nodes = graph.dijkstra_shortest_path(source, target)
        dijkstra_time = time.time() - start_time
        print("\nDijkstra Metrics:")
        if dijkstra_path:
            print(f"Path Length: {len(dijkstra_path) - 1}")
            print(f"Visited Nodes: {dijkstra_visited_nodes}")
            print(f"Execution Time: {dijkstra_time:.6f} seconds")
            get_path_data(dijkstra_path, rosters)
        else:
            print("No path found using Dijkstra's algorithm.")

    except Exception as e:
        print(f"Error during analysis: {e}")


def main():
    # File path to the dataset
    file_path = "nfl_rosters.csv"

    # Load the data
    rosters = load_data(file_path)

    # Build the graph
    graph = build_graph(rosters)

    # Compare
    compare_algorithms(graph, rosters)


if __name__ == "__main__":
    main()