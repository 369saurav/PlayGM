import React, { useState, useEffect } from "react";
import { ResultModal, ConfirmationModal } from "./Modal"; // Import the modals
import axios from 'axios'; // Import axios for API requests

const SideMenu = ({ onStartGame, onReset, gameStarted, notation }) => {
  const [selectedPlayer, setSelectedPlayer] = useState("");
  const [selectedColor, setSelectedColor] = useState("W");
  const [players, setPlayers] = useState([]); // State to store the list of players
  const [isResultModalOpen, setIsResultModalOpen] = useState(false);
  const [isConfirmationModalOpen, setIsConfirmationModalOpen] = useState(false);
  const [resultMessage, setResultMessage] = useState('');
  const [score, setScore] = useState('');

  useEffect(() => {
    // Fetch the list of players from the API when the component mounts
    axios.get('http://localhost:5000/playgm/players')
      .then(response => {
        console.log("API Response:", response.data); // Debugging line
        // Parse and set the players list
        const playersList = JSON.parse(response.data.players_list.replace(/'/g, '"'));
        console.log("Parsed Players List:", playersList); // Debugging line
        setPlayers(playersList);
      })
      .catch(error => {
        console.error("Error fetching players list:", error);
      });
  }, []);

  const handleStartGame = () => {
    onStartGame(selectedPlayer, selectedColor);
  };

  const handleResignGame = () => {
    setIsConfirmationModalOpen(true); // Open confirmation modal
  };

  const handleConfirmResign = () => {
    setIsConfirmationModalOpen(false); // Close confirmation modal
    setResultMessage('You have resigned from the game.');
    setScore(selectedColor === 'W' ? 'Black Won' : 'White Won'); // Update score based on color
    setIsResultModalOpen(true); // Open result modal
    onReset(); // Trigger reset from App.js
  };

  const handleCloseResultModal = () => {
    setIsResultModalOpen(false); // Close result modal
  };

  const handleCloseConfirmationModal = () => {
    setIsConfirmationModalOpen(false); // Close confirmation modal
  };

  const handleGameOver = (message, score) => {
    setResultMessage(message);
    setScore(score);
    setIsResultModalOpen(true); // Open result modal
  };

  return (
    <div className="w-[52%] mt-10">
      <form className="max-w-sm mx-auto">
        <label className="block mb-2 text-sm font-medium text-dark_green dark:text-dark_green">
          Choose a Player
        </label>
        <select
          id="players"
          className="bg-light_brown border border-dark_green text-dark_green text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
          value={selectedPlayer}
          onChange={(e) => setSelectedPlayer(e.target.value)}
          disabled={gameStarted} // Disable dropdown if game has started
        >
          {players.length > 0 ? (
            players.map((player, index) => (
              <option key={index} value={player}>{player}</option>
            ))
          ) : (
            <option value="" disabled>Loading players...</option>
          )}
        </select>
      </form>

      <form className="max-w-sm mx-auto mt-4">
        <label className="block mb-2 text-sm font-medium text-dark_green dark:text-dark_green">
          Choose a Color
        </label>
        <select
          id="colors"
          className="bg-light_brown border border-dark_green text-dark_green text-sm rounded-lg focus:ring-dark_green focus:border-dark_green block w-full p-2.5"
          value={selectedColor}
          onChange={(e) => setSelectedColor(e.target.value)}
          disabled={gameStarted} // Disable dropdown if game has started
        >
          <option value="W">White</option>
          <option value="B">Black</option>
        </select>
      </form>

      <div className="flex justify-center mt-8">
        <button
          type="button"
          className={`text-white ${gameStarted ? 'bg-red-700 hover:bg-red-800' : 'bg-dark_green hover:bg-blue-800'} font-medium rounded-lg text-sm px-8 py-2.5 mr-2`}
          onClick={gameStarted ? handleResignGame : handleStartGame}
        >
          {gameStarted ? 'Resign' : 'Start'}
        </button>
      </div>

      {/* Notation Display Box */}
      {gameStarted && (
        <div className="bg-dark_green p-4 mt-4 rounded-lg max-w-sm mx-auto">
          <h2 className="text-light_brown font-bold">Chess Notation</h2>
          <p className="mt-2 text-light_brown">{notation}</p>
        </div>
      )}

      <ConfirmationModal
        isOpen={isConfirmationModalOpen}
        onClose={handleCloseConfirmationModal}
        onConfirm={handleConfirmResign}
      />

      <ResultModal
        isOpen={isResultModalOpen}
        onClose={handleCloseResultModal}
        message={resultMessage}
        score={score}
      />
    </div>
  );
};

export default SideMenu;
