from services.embedding_service.create_embedding import get_embedding
from services.tidb_service.tidb_service import similarity_search
import chess.pgn

class PlaygmUsecase:

    def start_game(data):
        chess.Board
        return


    def  make_next_move(data):
        embedded_data = get_embedding(data.fen)
        similar_games = similarity_search(embedded_data)
        return