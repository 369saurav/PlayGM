import React, { useState } from "react";
import { ResultModal, ConfirmationModal } from "./Modal"; // Import the modals

const SideMenu = ({ onStartGame, onReset, gameStarted, notation }) => {
  const [selectedPlayer, setSelectedPlayer] = useState("Magnus Carlsen");
  const [selectedColor, setSelectedColor] = useState("W");
  const [isResultModalOpen, setIsResultModalOpen] = useState(false);
  const [isConfirmationModalOpen, setIsConfirmationModalOpen] = useState(false);
  const [resultMessage, setResultMessage] = useState('');
  const [score, setScore] = useState('');

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
        <label className="block mb-2 text-sm font-medium text--dark_green dark:text-dark_green">
          Choose a Player
        </label>
        <select
          id="players"
          className="bg-light_brown border border-dark_green text-dark_green text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
          value={selectedPlayer}
          onChange={(e) => setSelectedPlayer(e.target.value)}
          disabled={gameStarted} // Disable dropdown if game has started
        >
          <option value="Magnus Carlsen">Magnus Carlsen</option>
          {/* Add more players here */}
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
      <div className="bg-gray-100 p-4 mt-4 rounded-lg">
        <h2 className="text-lg font-bold">Chess Notation</h2>
        <p className="mt-2">{notation}</p>
      </div>

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
