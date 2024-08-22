import React, { useState } from "react";
import PlayerVsComputerChessboard from "./components/PlayerVsComputerChessboard";
import "./App.css";
import SideMenu from "./components/SideMenu";

function App() {
  const [selectedPlayer, setSelectedPlayer] = useState("Magnus Carlsen");
  const [selectedColor, setSelectedColor] = useState("W");
  const [gameStarted, setGameStarted] = useState(false);
  const [notation, setNotation] = useState(''); // State for chess notation

  const handleStartGame = (player, color) => {
    setSelectedPlayer(player);
    setSelectedColor(color);
    setGameStarted(true); // Set game started state to true
  };

  const handleReset = () => {
    setGameStarted(false); // Set game started state to false
    setNotation(''); // Reset chess notation
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
          />
        </div>
      </div>
    </>
  );
}

export default App;
