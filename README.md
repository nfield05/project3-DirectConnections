NFL Direct Connections

This project visualizes connections between NFL players based on their shared teams and seasons. It allows users to analyze relationships using shortest path algorithms (BFS and Dijkstra), explore player statistics, and view insights from the dataset.

Features

Shortest Path Algorithms: Find the shortest path between two players using BFS or Dijkstra's algorithm.

Insights Dashboard:

Most connected players.

Teams with the most players.

Players with the longest careers.

Dataset Toggle: Switch between real (nfl_rosters.csv) and expanded (expanded_nfl_rosters.csv) datasets.

Installation

Prerequisites

Python 3.9 or higher

Streamlit

Required Python packages:

pandas

streamlit

faker (optional, if generating synthetic data)

nfl_data_py

time

collections

ssl


Steps

Clone this repository or download the project files:

bash

git clone <repository-urlhttps://github.com/nfield05/project3-DirectConnections>



Ensure you have the datasets:

Real Dataset: nfl_rosters.csv

Expanded Dataset: expanded_nfl_rosters.csv

Place these files in the same directory as the app.


Running the Application

Start the Streamlit app:

bash

streamlit run app.py

Open the app in your browser:
The app will automatically open in your default web browser. If it doesn't, navigate to the URL shown in your terminal.

Using the Application

Dataset Selection
Use the sidebar to select between the "Real Dataset" and the "Expanded Dataset".
Shortest Path Algorithms
Select a source player and a target player from the dropdowns.
Run either:

BFS Algorithm: For unweighted shortest path.

Dijkstra Algorithm: For weighted shortest path.

View results:
Path length, visited nodes, and execution time.
Step-by-step connections between players.

Insights Dashboard

Toggle the Insights Dashboard from the sidebar to view:

Most Connected Players.

Teams with the Most Players.

Players with Longest Careers.

