from crypt import methods

from flask import Flask, request, jsonify
import services.embedding_service.create_embedding

import mysql.connector
from mysql.connector import Error

from core.usecase.playgm_usecase import *
from services.embedding_service.create_embedding import get_embedding
from services.tidb_service.tidb_service import similarity_search

main_router = Flask(__name__)


@main_router.route('/playgm/start', methods=['POST'])
def start_game():
    request_body = request.json
    PlaygmUsecase.start_game(request_body)
    return jsonify({"message": "Game Started!"}), 201

#Handler for every player's move
@main_router.route('/playgm/move', methods=['POST'])
def players_move():
    request_body = request.json
    next_move = PlaygmUsecase.make_next_move(request_body)

    if next_move is None:
        return jsonify({"message": "Failed!","next_move":None}), 400
    else:
        return jsonify({"message": "Embedding created successfully!", "next_move": next_move}), 201


