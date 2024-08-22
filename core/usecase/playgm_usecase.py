# import os
#
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_google_genai import ChatGoogleGenerativeAI

from services.embedding_service.create_embedding import get_embedding
from services.tidb_service.tidb_service import similarity_search
import chess
import chess.engine

# import mysql.connector
# from mysql.connector import Error


def start_game(data):
    chess_board = chess.Board
    chess_board.fen(data.fen)
    return


def make_next_move(fen, move_number, player_name, player_colour):
    embedded_data = get_embedding(fen)
    print(str(embedded_data))
    generate_response(fen)
    similar_games = similarity_search(str(embedded_data))
    print("Similar_games::: "+str(similar_games))
    print("fen:: "+fen)
    chess_board = chess.Board(fen)
    if chess_board.is_game_over():
        if chess_board.is_fifty_moves():
            print("Draw by fifty-move rule")
        elif chess_board.is_stalemate():
            print("Draw by stalemate")
        elif chess_board.can_claim_threefold_repetition():
            print("Draw by threefold repetition")
        elif chess_board.is_insufficient_material():
            print("Draw by insufficient material")
        else:
            print("Game over")
    else:
        # Generate a list of legal moves
        legal_moves = list(chess_board.legal_moves)
        fen_moves = []
        for similar_fen in similar_games:
            fen_move = fen_to_move(similar_fen['opponent_fen'],similar_fen['player_fen'])
            print("fen_move::: "+str(fen_move))
            fen_moves.append(fen_move)



        print(str(legal_moves))

        if legal_moves:
            return fen_to_move(fen,generate_response(fen))

            # For demonstration, let's just use the first legal move
            # for m in fen_moves:
            #     if chess_board.is_legal(m):
            #         n_fen = chess_board.fen()
            #         print(f"New position from similar games: {n_fen}")
            #         return m
            #
            # move = legal_moves[0]
            # if chess_board.is_legal(move):
            #     print(f"Legal move: {move}")
            #     # Make the move
            #     chess_board.push(move)
            #     # Get the new FEN after the move
            #     new_fen = chess_board.fen()
            #     print(f"New position: {new_fen}")
            #     return move
            # else:
            #     print("No legal moves available")


    return


def fen_to_move(from_fen , to_fen):
    board1 = chess.Board(from_fen)
    # board2 = chess.Board(to_fen)
    print("from_fen::: "+str(from_fen)+" :: to_fen::: "+str(to_fen))
    # Generate all legal moves from the first position
    for move in board1.legal_moves:
        print("move:: fen_to_move::: "+str(move))
        # Apply the move to a copy of the first board
        test_board = board1.copy()
        test_board.push(move)
        print("fen_to_move test_board::: "+str(test_board.fen())+"  :: to_fen::: "+str(to_fen))
        # If the resulting position matches the second FEN, we've found our move
        if test_board.fen().split(' ')[0] == to_fen.split(' ')[0]:
            return move



    # def is_move_legal(self,opponent_fen, your_fen):
    #     # Create board from opponent's FEN
    #     board = chess.Board(opponent_fen)
    #
    #     # Create board from your FEN
    #     your_board = chess.Board(your_fen)
    #
    #     # Find the difference between the two positions
    #     moves = list(board.legal_moves)
    #     for move in moves:
    #         board.push(move)
    #         # Compare relevant parts of FEN strings
    #         if board.board_fen() == your_board.board_fen() and board.turn == your_board.turn:
    #             return True, f"Legal move: {move}"
    #         board.pop()
    #
    #     # If we didn't find a matching move, it's not legal
    #     return False, "Illegal move"


# def generate_response(current_fen):
#     # Perform the similarity search
#     current_fen_embedding = get_embedding(current_fen)
#     similar_positions = similarity_search(str(current_fen_embedding))
#
#     # Construct the context for the prompt
#     context = "\n".join([f"Player's move: {pos['player_fen']} Opponent's move: {pos['opponent_fen']}"
#                          for pos in similar_positions])
#
#     # Prompt with the context and current FEN
#     prompt = ChatPromptTemplate.from_messages(
#         [
#             ("system",
#              "You are a Chess Player. You will be given a FEN of the current chess position, and you need to suggest the next move for the current player. "
#              "Your task is to choose the best move from the provided player moves or generate your own move in FEN format. "
#              "For example, if White plays e4 and Black responds with e5, the FEN should update from "
#              "'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1' to "
#              "'rnbqkbnr/pppp1ppp/8/4p3/8/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2'. "
#              "Return only the updated FEN string after making the move, with no additional text or descriptions."),
#             ("user",
#              f"FEN-CONTEXT:\n{context}\nCURRENT-FEN: {current_fen}")
#         ]
#     )
#
#     google_api_key = os.environ.get('GOOGLE_API_KEY')
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-1.5-flash",
#         temperature=0.4,
#         max_retries=2,
#         api_key=google_api_key
#     )
#     output_parser = StrOutputParser()
#     chain = prompt | llm | output_parser
#
#     # Generate response from the chain
#     response = chain.invoke({"context": context, "current_fen": current_fen})
#
#     print("response::: " + str(response))
#     return response

def generate_response(current_fen):
    # Initialize the chess board from the current FEN
    board = chess.Board(current_fen)

    # Define the path to the Stockfish executable
    stockfish_path = "D:/stockfish-windows-x86-64-avx2/stockfish/stockfish-windows-x86-64-avx2.exe"

    # Use a context manager to open and close the Stockfish engine
    try:
        with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
            result = engine.play(board, chess.engine.Limit(time=2.0))
            best_move = result.move
    except Exception as e:
        print(f"An error occurred while running Stockfish: {e}")
        return current_fen  # Return the current FEN if there's an error

    # Update the board with the best move
    board.push(best_move)

    # Get the updated FEN after the move
    updated_fen = board.fen()
    print("response::: "+updated_fen)
    # Return the updated FEN
    return updated_fen