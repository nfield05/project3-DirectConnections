import streamlit as st
import pandas as pd
from nfl_teammates_graph import Graph, load_data, build_graph
import time

# Dataset selector
st.sidebar.title("Dataset Selection")
dataset_choice = st.sidebar.radio(
    "Choose the dataset to analyze:",
    options=["Real Dataset", "Expanded Dataset"],
    index=0
)

# Determine file path based on selection
if dataset_choice == "Real Dataset":
    file_path = "nfl_rosters.csv"
else:
    file_path = "expanded_nfl_rosters.csv"

# Load data and build the graph
try:
    rosters = load_data(file_path)
    st.success(f"Data Loaded Successfully from `{file_path}`!")
    st.write(f"**Data Summary:** {rosters.shape[0]} rows, {rosters.shape[1]} columns")
    graph = build_graph(rosters)
    st.success("Graph built successfully.")
except FileNotFoundError:
    st.error(f"The file `{file_path}` was not found. Please ensure the file exists.")
    st.stop()

# Create player mappings for the search bar
player_mapping = rosters[['player_name', 'player_id']].dropna().drop_duplicates().set_index('player_name').to_dict()['player_id']
id_to_name_mapping = rosters[['player_name', 'player_id']].dropna().drop_duplicates().set_index('player_id').to_dict()['player_name']
player_names = list(player_mapping.keys())


if "bfs_results" not in st.session_state:
    st.session_state.bfs_results = None
if "dijkstra_results" not in st.session_state:
    st.session_state.dijkstra_results = None
if "explore_data" not in st.session_state:
    st.session_state.explore_data = None
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navigation buttons
def go_to_explore(player1, player2):
    """Navigate to the explore page with player stats."""
    st.session_state.explore_data = {"player1": player1, "player2": player2}
    st.session_state.page = "explore"

def reset_app():
    """Reset the app to its initial state."""
    for key in st.session_state.keys():
        del st.session_state[key]  # Clear all session state variables
    st.session_state.page = "home"  # Set page back to home
    st.query_params = {}  # Reset query parameters
def generate_insights(rosters):
    st.markdown("## Insights Dashboard")

    # Most Connected Players
    st.markdown("### Most Connected Players")
    connections = rosters.groupby("player_id").size().sort_values(ascending=False).head(10)
    player_names = [id_to_name_mapping.get(pid, pid) for pid in connections.index]
    insights_df = pd.DataFrame({"Player": player_names, "Connections": connections.values})
    st.dataframe(insights_df)

    # Teams with the Most Players
    st.markdown("### Teams with the Most Players")
    team_counts = rosters.groupby("team").size().sort_values(ascending=False).head(10)
    st.bar_chart(team_counts)

    # Longest Careers
    st.markdown("### Players with Longest Careers")
    career_lengths = rosters.groupby("player_id")["season"].nunique().sort_values(ascending=False).head(10)
    career_df = pd.DataFrame({
        "Player": [id_to_name_mapping.get(pid, pid) for pid in career_lengths.index],
        "Seasons": career_lengths.values
    })
    st.dataframe(career_df)

# Main UI
if st.session_state.page == "home":
    st.title("NFL Direct Connections")

    # Input players here
    source_player_name = st.selectbox("Search and Select Source Player Name:", options=player_names)
    target_player_name = st.selectbox("Search and Select Target Player Name:", options=player_names)

    source_player_id = player_mapping.get(source_player_name, None)
    target_player_id = player_mapping.get(target_player_name, None)

    # Algorithm Buttons and Results
    if source_player_id and target_player_id:
        col1, col2 = st.columns(2)

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

        # BFS Results
        if st.session_state.bfs_results:
            st.markdown("## BFS Algorithm Results:")
            results = st.session_state.bfs_results
            st.write(f"**Path Length:** {len(results['path']) - 1}")
            st.write(f"**Visited Nodes:** {results['visited_nodes']}")
            st.write(f"**Execution Time:** {results['execution_time']:.6f} seconds")

            # Path Details
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
                    if st.button(f"Explore Connection {i + 1} (BFS)", key=f"bfs_explore_{i}"):
                        go_to_explore(player1_name, player2_name)

        # Dijkstra Results
        if st.session_state.dijkstra_results:
            st.markdown("## Dijkstra Algorithm Results:")
            results = st.session_state.dijkstra_results
            st.write(f"**Path Length:** {len(results['path']) - 1}")
            st.write(f"**Visited Nodes:** {results['visited_nodes']}")
            st.write(f"**Execution Time:** {results['execution_time']:.6f} seconds")

            # Path Details
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
                    if st.button(f"Explore Connection {i + 1} (Dijkstra)", key=f"dijkstra_explore_{i}"):
                        go_to_explore(player1_name, player2_name)


        if st.button("Try a New Connection?"):
            reset_app()
        if st.sidebar.checkbox("Show Insights Dashboard"):
            generate_insights(rosters)

elif st.session_state.page == "explore":
    # Explore Page
    explore_data = st.session_state.explore_data
    if explore_data:
        player1 = explore_data["player1"]
        player2 = explore_data["player2"]

        st.title("Explore Connection")
        st.markdown(f"### {player1}'s Stats:")
        st.write(rosters[rosters["player_name"] == player1])
        st.markdown(f"### {player2}'s Stats:")
        st.write(rosters[rosters["player_name"] == player2])

    if st.button("Back to Results", key="back_to_results"):
        st.session_state.page = "home"
