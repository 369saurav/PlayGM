from crypt import methods

from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
from core.usecase.playgm_usecase import *
main_router = Flask(__name__)


@main_router.route('/playgm/start', methods=['POST'])
def start_game():
    request_body = request.json
    start_game()
    return jsonify({"message": "Game Started!"}), 201

#Handler for every player's move
@main_router.route('/playgm/move', methods=['POST'])
def players_move():
    request_body = request.json
    fen = request_body['fen']
    # move_number = int(request_body['move_number'])
    # player_name = request_body['player_name']
    # player_colour = request_body['player_colour']
    usecase_parameter = (fen,'move_number','player_colour','player_colour')
    # pl = PlaygmUsecase()
    next_move = make_next_move(fen,'move_number','player_colour','player_colour')
    print("next MOVE::: "+str(next_move))
    if next_move is None:
        return jsonify({"message": "Failed!","next_move":None}), 400
    else:
        return jsonify({"move":str(next_move)}), 201

@main_router.route('/playgm/players', methods=['GET'])
def get_players_list():
    player_list = fetch_all_players()
    return jsonify({"players_list":str(player_list)}), 200

# @main_router.route('/playgm/move', methods=['GET'])
# def players_move():
#     print("PLAYER MOVED:::")
#     fen = request.args.get('fen')  # Get 'fen' from query parameters
#
#     if not fen:
#         return jsonify({"message": "Missing 'fen' parameter"}), 400
#
#     # Assuming PlaygmUsecase and make_next_move are defined as in your original setup
#     pl = PlaygmUsecase()
#     next_move = pl.make_next_move(fen,'','','')
#
#     if next_move is None:
#         return jsonify({"message": "Failed!", "next_move": None}), 400
#     else:
#         return jsonify({"next_move": next_move}), 200

CORS(main_router)  # Enable CORS for all routes


# @main_router.route('/playgm/move', methods=['GET', 'OPTIONS'])
# def players_move():
#     if request.method == 'OPTIONS':
#         # Handle preflight request
#         print("PLAYER MOVED [OPTIONS]:::")
#         return '', 200
#
#     # Handle GET request
#     fen = request.args.get('fen')
#     print("PLAYER MOVED [GET]:::")
#
#     if not fen:
#         return jsonify({"message": "Missing 'fen' parameter"}), 400
#
#     # Assuming PlaygmUsecase and make_next_move are defined as in your original setup
#     pl = PlaygmUsecase()
#     next_move = pl.make_next_move(fen,'','','')
#
#     if next_move is None:
#         return jsonify({"message": "Failed!", "next_move": None}), 400
#     else:
#         return jsonify({"move": str(next_move)}), 200

if __name__ == '__main__':
    main_router.run(host='0.0.0.0',port=5000, debug=True)
