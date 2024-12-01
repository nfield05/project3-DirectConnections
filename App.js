import React, { useState } from "react";
import Header from "./components/Header";
import PlayerInput from "./components/PlayerInput";
import ConnectionResult from "./components/ConnectionResult";
import "./App.css";

const App = () => {
  const initialState = {
    player1: "",
    player2: "",
    connections: [],
  };

  const [state, setState] = useState(initialState);

  const findConnection = () => {
    // Example logic to simulate connections
    const exampleConnections = [
      `${state.player1} is connected to Player 1 through Example Team`,
      `Player 1 is connected to Player 2 through Example Team`,
      `Player 2 is connected to ${state.player2} through Example Team`,
    ];
    setState({ ...state, connections: exampleConnections });
  };

  const resetApp = () => {
    setState(initialState); // Reset the state to its initial values
  };

  return (
      <div className="App">
        <Header />
        <div className="input-section">
          <PlayerInput
              label="Enter Your First Player Here"
              onChange={(e) =>
                  setState({ ...state, player1: e.target.value })
              }
          />
          <PlayerInput
              label="Enter Your Second Player Here"
              onChange={(e) =>
                  setState({ ...state, player2: e.target.value })
              }
          />
          <button onClick={findConnection}>Find The Connection!</button>
        </div>
        {state.connections.length > 0 && (
            <ConnectionResult
                player1={state.player1}
                player2={state.player2}
                connections={state.connections}
                onReset={resetApp}
            >
              <button onClick={resetApp}>Try Another Connection?</button>
            </ConnectionResult>
        )}
      </div>
  );
};

export default App;
