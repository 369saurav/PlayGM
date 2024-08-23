import React, { useState } from "react";
import PlayerVsComputerChessboard from "./components/PlayerVsComputerChessboard";
import "./App.css";
import SideMenu from "./components/SideMenu";
import {ResultModal, ConfirmationModal} from "./components/Modal"

function App() {
  const [selectedPlayer, setSelectedPlayer] = useState("Magnus Carlsen");
  const [selectedColor, setSelectedColor] = useState("W");
  const [gameStarted, setGameStarted] = useState(false);
  const [notation, setNotation] = useState(''); // State for chess notation
  const [score, setScore] = useState('');
  const [isResultModalOpen, setIsResultModalOpen] = useState(false);
  const [resultMessage, setResultMessage] = useState('');

  const handleStartGame = (player, color) => {
    setSelectedPlayer(player);
    setSelectedColor(color);
    setGameStarted(true); // Set game started state to true
  };

 const handleReset = () => {
    setGameStarted(false); // Set game started state to false
    setNotation(''); // Reset chess notation
    setScore(''); // Clear score when resetting
    setIsResultModalOpen(false); // Ensure the result modal is closed
  };

  const handleMove = (move) => {
    setNotation(prevNotation => {
      let newMove;
  
      if (Array.isArray(move)) {
        // Get the 'lan' value from the first element of the array
        newMove = move[0].lan;
      } else if (typeof move === 'string') {
        // If move is already a string, use it directly
        newMove = move;
      }
  
      const newNotation = `${prevNotation} ${newMove}`;
      
      console.log(newNotation.trim());
      console.log(move);
      console.log(prevNotation);
  
      return newNotation.trim(); // Remove any extra whitespace
    });
  };
const handleGameOver = (result) => {
    let message, gameScore;
    if (result === '1-0') {
      message = 'White wins by checkmate!';
      gameScore = 'White Won';
    } else if (result === '0-1') {
      message = 'Black wins by checkmate!';
      gameScore = 'Black Won';
    } else if (result === 'D') {
      message = 'The game is a draw.';
      gameScore = 'Draw';
    }

   setResultMessage(message);
    setScore(gameScore);
    setIsResultModalOpen(true); // Open result modal
  };
    const handleCloseResultModal = () => {
    setIsResultModalOpen(false); // Close result modal
    handleReset(); // Optionally reset the game state or do other cleanup
  };
  return (
    <>
      <div className="bg-dark_green pb-4 pt-1 pl-3">
        <h1 className="text-light_brown text-4xl font-bold">PLAY-GM</h1>
      </div>
      <div className="w-[100%] bg-light_brown">
        <div className="flex mt-0 lg:flex-row sm:flex-col">
          <SideMenu
            onStartGame={handleStartGame}
            onReset={handleReset}
            gameStarted={gameStarted} // Pass gameStarted state
            notation={notation} // Pass notation to SideMenu
          />
          <PlayerVsComputerChessboard
            selectedPlayer={selectedPlayer}
            selectedColor={selectedColor}
            reset={!gameStarted} // Reset board if game is not started
            onMove={handleMove} // Pass handleMove function
            onGameOver={handleGameOver} // Pass handleGameOver function

          />
        </div>
      </div>
      <ResultModal
        isOpen={isResultModalOpen}
        onClose={handleCloseResultModal} // Use the close handler
        message={resultMessage}
        score={score}
      />
    </>
  );
}

export default App;
