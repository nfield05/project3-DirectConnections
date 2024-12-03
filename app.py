import streamlit as st
import pandas as pd
from nfl_teammates_graph import Graph, load_data, build_graph
import time

# Load data and build the graph
file_path = "nfl_rosters.csv"

try:
    rosters = load_data(file_path)
    st.success("Data Loaded Successfully!")
    st.write(f"**Data Summary:** {rosters.shape[0]} rows, {rosters.shape[1]} columns")
    graph = build_graph(rosters)
    st.success("Graph built successfully.")
except FileNotFoundError:
    st.error("The file 'nfl_rosters.csv' was not found. Please generate it using 'nfl_dataset.py'.")
    st.stop()

# Create player mappings
player_mapping = rosters[['player_name', 'player_id']].dropna().drop_duplicates().set_index('player_name').to_dict()['player_id']
id_to_name_mapping = rosters[['player_name', 'player_id']].dropna().drop_duplicates().set_index('player_id').to_dict()['player_name']
player_names = list(player_mapping.keys())

# Initialize session state
if "bfs_results" not in st.session_state:
    st.session_state.bfs_results = None
if "dijkstra_results" not in st.session_state:
    st.session_state.dijkstra_results = None
if "explore_data" not in st.session_state:
    st.session_state.explore_data = None
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navigation Functions
def go_to_explore(player1, player2):
    """Navigate to the explore page."""
    st.session_state.explore_data = {"player1": player1, "player2": player2}
    st.session_state.page = "explore"

def reset_app():
    """Reset the app to its initial state."""
    st.session_state.bfs_results = None
    st.session_state.dijkstra_results = None
    st.session_state.explore_data = None
    st.session_state.page = "home"

# Main UI
if st.session_state.page == "home":
    st.title("NFL Direct Connections")

    # Searchable input for Source and Target Players
    source_player_name = st.selectbox("Search and Select Source Player Name:", options=player_names, help="Start typing the player's name.")
    target_player_name = st.selectbox("Search and Select Target Player Name:", options=player_names, help="Start typing the player's name.")

    # Convert names to IDs
    source_player_id = player_mapping.get(source_player_name, None)
    target_player_id = player_mapping.get(target_player_name, None)

    # Algorithm Buttons
    col1, col2 = st.columns(2)

    if source_player_id and target_player_id:
        with col1:
            if st.button("Run BFS Algorithm"):
                start_time = time.time()
                path, visited_nodes = graph.bfs_shortest_path(source_player_id, target_player_id)
                exec_time = time.time() - start_time

                if path:
                    st.session_state.bfs_results = {
                        "path": path,
                        "visited_nodes": visited_nodes,
                        "execution_time": exec_time,
                    }
                else:
                    st.error("No path found using BFS.")

        with col2:
            if st.button("Run Dijkstra Algorithm"):
                start_time = time.time()
                path, visited_nodes = graph.dijkstra_shortest_path(source_player_id, target_player_id)
                exec_time = time.time() - start_time

                if path:
                    st.session_state.dijkstra_results = {
                        "path": path,
                        "visited_nodes": visited_nodes,
                        "execution_time": exec_time,
                    }
                else:
                    st.error("No path found using Dijkstra.")

        # Display Results
        if st.session_state.bfs_results:
            st.markdown("## BFS Algorithm Results:")
            results = st.session_state.bfs_results
            st.write(f"**Path Length:** {len(results['path']) - 1}")
            st.write(f"**Visited Nodes:** {results['visited_nodes']}")
            st.write(f"**Execution Time:** {results['execution_time']:.6f} seconds")

            # Display detailed path with "Explore Connection" buttons
            st.markdown("### Path Details (BFS):")
            for i in range(len(results['path']) - 1):
                player1_id = results['path'][i]
                player2_id = results['path'][i + 1]
                player1_name = id_to_name_mapping.get(player1_id, player1_id)
                player2_name = id_to_name_mapping.get(player2_id, player2_id)
                common_team = pd.merge(
                    rosters[rosters['player_id'] == player1_id],
                    rosters[rosters['player_id'] == player2_id],
                    on=['team', 'season']
                )

                if not common_team.empty:
                    team = common_team.iloc[0]['team']
                    year = common_team.iloc[0]['season']
                    st.write(f"{player1_name} played with {player2_name} on the {year} {team}.")
                    if st.button(f"Explore Connection {i + 1}", key=f"explore_{i}"):
                        go_to_explore(player1_name, player2_name)

        if st.session_state.dijkstra_results:
            st.markdown("## Dijkstra Algorithm Results:")
            results = st.session_state.dijkstra_results
            st.write(f"**Path Length:** {len(results['path']) - 1}")
            st.write(f"**Visited Nodes:** {results['visited_nodes']}")
            st.write(f"**Execution Time:** {results['execution_time']:.6f} seconds")

            # Display detailed path with "Explore Connection" buttons
            st.markdown("### Path Details (Dijkstra):")
            for i in range(len(results['path']) - 1):
                player1_id = results['path'][i]
                player2_id = results['path'][i + 1]
                player1_name = id_to_name_mapping.get(player1_id, player1_id)
                player2_name = id_to_name_mapping.get(player2_id, player2_id)
                common_team = pd.merge(
                    rosters[rosters['player_id'] == player1_id],
                    rosters[rosters['player_id'] == player2_id],
                    on=['team', 'season']
                )

                if not common_team.empty:
                    team = common_team.iloc[0]['team']
                    year = common_team.iloc[0]['season']
                    st.write(f"{player1_name} played with {player2_name} on the {year} {team}.")
                    if st.button(f"Explore Connection {i + 1}", key=f"explore_{i}"):
                        go_to_explore(player1_name, player2_name)

elif st.session_state.page == "explore":
    explore_data = st.session_state.explore_data
    if explore_data:
        player1 = explore_data["player1"]
        player2 = explore_data["player2"]
        st.title("Explore Connection")
        st.write(f"### {player1}'s Stats:")
        st.write(rosters[rosters["player_name"] == player1])
        st.write(f"### {player2}'s Stats:")
        st.write(rosters[rosters["player_name"] == player2])

    if st.button("Back to Results"):
        st.session_state.page = "home"
