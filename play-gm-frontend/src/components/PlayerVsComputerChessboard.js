import React, { useState, useEffect } from 'react';
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js';
import axios from 'axios';

const PlayerVsComputerChessboard = ({ selectedPlayer, selectedColor, reset, onMove, onGameOver }) => {
  const [game, setGame] = useState(new Chess());
  const [fen, setFen] = useState('start');
  const [boardOrientation, setBoardOrientation] = useState('white');
  const [gameOver, setGameOver] = useState('score')
  const [isResultModalOpen, setIsResultModalOpen] = useState(false);
  const [isThinking, setIsThinking] = useState(false); // State for thinking animation

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
      setIsThinking(true); // Start thinking animation

      try {
        const response = await axios.post('http://127.0.0.1:5000/playgm/move', { fen: game.fen() });
        const computerMove = response.data.move;
        setIsThinking(false); // Stop thinking animation
        if (computerMove == '0-1') {
          handleGameOver('0-1')
        }
        else if (computerMove == '1-0') {
          handleGameOver('1-0')
        }
        else if (computerMove == 'D') {
          handleGameOver('D')
        }
        else {
          game.move(computerMove);
          setGame(new Chess(game.fen()));
          setFen(game.fen());
          onMove(game.history({ verbose: true }));
          if (/-D$/.test(computerMove)) {
            handleGameOver('D')
  
          } else if (/-0-1$/.test(computerMove)) {
            handleGameOver('0-1')
          } else if (/-1-0$/.test(computerMove)) {
            handleGameOver('1-0')
          }
        }


      } catch (error) {
        console.error('Error fetching computer move:', error);
        setIsThinking(false);
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
      onMove(`${move.from}${move.to}`); // Format user move as "e2-e4"
      return true;
    }
    return false;
  };

  const handleGameOver = (score) => {

    onGameOver(score);
    reset();
  };

  const handleCloseResultModal = () => {
    setIsResultModalOpen(false); // Close result modal
  };


  return (
    <div className='w-[38%] sm:py-4 float-right'>
      <div className="bg-[#f0d9b5] text-[#b58863] p-2 text-left font-bold">
        {selectedPlayer} {isThinking && <span className="thinking">is thinking</span>}
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
        You
      </div>
    </div>
  );
};

export default PlayerVsComputerChessboard;
