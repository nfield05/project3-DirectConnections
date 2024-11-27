const ConnectionResult = ({ player1, player2, connections, onReset }) => {
    return (
        <div className="connection-result">
            <h2>Direct Connections</h2>
            <div className="connection-path">
                <span>{player1}</span>
                <span>➡</span>
                <span>{player2}</span>
            </div>
            <p>These Players are linked through {connections.length} connections</p>
            <div className="connection-details">
                {connections.map((connection, index) => (
                    <div key={index} className="connection-step">
                        <p>{connection}</p>
                    </div>
                ))}
            </div>
            <button onClick={onReset}>Try Another Connection?</button>
        </div>
    );
};

export default ConnectionResult;
