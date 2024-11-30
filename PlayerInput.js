// PlayerInput.js
const PlayerInput = ({ label, onChange }) => {
    return (
        <div className="player-input-container">
            <input
                type="text"
                placeholder={label}
                onChange={onChange}
                className="player-input" /* Attach the class here */
            />
        </div>
    );
};

export default PlayerInput;
