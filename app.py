import streamlit as st
import pandas as pd
from nfl_teammates_graph import Graph, load_data, build_graph

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "opening"
if "source_player" not in st.session_state:
    st.session_state.source_player = ""
if "target_player" not in st.session_state:
    st.session_state.target_player = ""
if "algorithm" not in st.session_state:
    st.session_state.algorithm = ""
if "connection_path" not in st.session_state:
    st.session_state.connection_path = []
if "no_connection" not in st.session_state:
    st.session_state.no_connection = False


# Navigation functions
def go_to_results(algorithm):
    st.session_state.algorithm = algorithm
    st.session_state.page = "results"


def reset_app():
    st.session_state.page = "opening"
    st.session_state.source_player = ""
    st.session_state.target_player = ""
    st.session_state.algorithm = ""
    st.session_state.connection_path = []
    st.session_state.no_connection = False


# Load CSV data
file_path = "nfl_rosters.csv"
try:
    rosters = load_data(file_path)
    graph = build_graph(rosters)
except FileNotFoundError:
    st.error("The file 'nfl_rosters.csv' was not found. Please generate it using 'nfl_dataset.py'.")
    st.stop()

# Opening Page
if st.session_state.page == "opening":
    st.title("NFL Direct Connections")

    # Input fields for players
    st.write("Enter the players you want to connect:")
    source_player = st.text_input("Source Player", value=st.session_state.source_player)
    target_player = st.text_input("Target Player", value=st.session_state.target_player)

    st.session_state.source_player = source_player
    st.session_state.target_player = target_player

    # Header for algorithm selection
    st.markdown("## Find Your Connection through the...")

    # Algorithm buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("BFS Algorithm"):
            path, _ = graph.bfs_shortest_path(source_player, target_player)
            if path:
                st.session_state.connection_path = path
                go_to_results("BFS")
            else:
                st.session_state.no_connection = True
                go_to_results("BFS")
    with col2:
        st.markdown("<p style='text-align: center;'>or</p>", unsafe_allow_html=True)
    with col3:
        if st.button("Dijkstra Algorithm"):
            path, _ = graph.dijkstra_shortest_path(source_player, target_player)
            if path:
                st.session_state.connection_path = path
                go_to_results("Dijkstra")
            else:
                st.session_state.no_connection = True
                go_to_results("Dijkstra")

# Results Page
elif st.session_state.page == "results":
    st.title("NFL Direct Connections")

    st.markdown(f"### {st.session_state.algorithm} Results...")
    st.write(f"**Source Player:** {st.session_state.source_player}")
    st.write(f"**Target Player:** {st.session_state.target_player}")

    if st.session_state.no_connection:
        st.error("No connections found between the selected players. Please try again.")
        if st.button("Try Another Connection?"):
            reset_app()
    else:
        st.markdown(f"### These Players are linked through {len(st.session_state.connection_path) - 1} connections.")

        # Display the connection path
        for i in range(len(st.session_state.connection_path) - 1):
            player1 = st.session_state.connection_path[i]
            player2 = st.session_state.connection_path[i + 1]

            # Find the common team and year for these players
            player1_data = rosters[rosters['player_id'] == player1]
            player2_data = rosters[rosters['player_id'] == player2]
            common_team = pd.merge(player1_data, player2_data, on=['team', 'season'])

            if not common_team.empty:
                team = common_team.iloc[0]['team']
                year = common_team.iloc[0]['season']
                st.markdown(f"#### {player1} → {player2}")
                st.markdown(f"Through {team} ({year})")
            else:
                st.markdown(f"#### {player1} → {player2}")
                st.markdown("No common team or season found.")

        if st.button("Try Another Connection?"):
            reset_app()
