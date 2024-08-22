import React, { useState, useEffect } from 'react';
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js';
import axios from 'axios';

const PlayerVsComputerChessboard = ({ selectedPlayer, selectedColor, reset, onMove }) => {
  const [game, setGame] = useState(new Chess());
  const [fen, setFen] = useState('start');
  const [boardOrientation, setBoardOrientation] = useState('white');

  useEffect(() => {
    setBoardOrientation(selectedColor === 'W' ? 'white' : 'black');
  }, [selectedColor]);

  useEffect(() => {
    if (reset) {
      // Reset the board when the reset prop changes
      setGame(new Chess());
      setFen('start');
      return; // Exit useEffect
    }

    const makeComputerMove = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5000/playgm/move', { fen: game.fen() });
        const computerMove = response.data.move;
        game.move(computerMove);
        setGame(new Chess(game.fen()));
        setFen(game.fen());
        onMove(game.history({ verbose: true })); // Notify about moves
      } catch (error) {
        console.error('Error fetching computer move:', error);
      }
    };

    if (game.turn() === (selectedColor === 'W' ? 'b' : 'w')) {
      makeComputerMove();
    }
  }, [game, selectedColor, reset, onMove]);

  const handleMove = (sourceSquare, targetSquare, piece) => {
    if (reset) {
      return false; // Don't handle moves if the game is over or resetting
    }
  
    let move = null;
  try {
    move = game.move({
      from: sourceSquare,
      to: targetSquare,
      promotion: piece[1].toLowerCase() ?? "q",
    });
  } catch {
    console.log("Invalid move");
  }

  if (move) {
    setGame(new Chess(game.fen()));
    setFen(game.fen());
    onMove(`${move.from}-${move.to}`); // Format user move as "e2-e4"
    return true;
  }
  return false;
  };
  

  return (
    <div className='w-[38%] sm:py-4 float-right'>
      <div className="bg-[#f0d9b5] text-[#b58863] p-2 text-left font-bold">
        {selectedPlayer}
      </div>
      <Chessboard
        id="example-chess-board"
        position={fen}
        onPieceDrop={handleMove}
        boardOrientation={boardOrientation}
        customBoardStyle={{
          borderRadius: '0px',
        }}
      />
      <div className="bg-[#f0d9b5] text-[#b58863] p-2 text-left font-bold">
        Guest
      </div>
    </div>
  );
};

export default PlayerVsComputerChessboard;
