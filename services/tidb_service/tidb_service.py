from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
            port=4000,
            user="3CHjZydnDAbyLy6.root",
            password="LJIBsOyh00RIQLC0",
            database="test",
            ssl_ca="isrgrootx1.pem",
            ssl_verify_cert=True,
            ssl_verify_identity=True
        )
        return connection
    except Error as e:
        print(f"Error connecting to TiDB: {e}")
        return None


def similarity_search(embedding, limit=5):
    connection = get_db_connection()
    results = []
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)

            query = """
            SELECT id, player_name, opponent_name, game_date, player_piece_color, chess_annotation,
                   embedding <=> %s AS distance
            FROM chess_games
            ORDER BY embedding <=> %s
            LIMIT %s
            """

            cursor.execute(query, (embedding, embedding, limit))
            results = cursor.fetchall()

        except Error as error:
            print(f"Error executing query: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    return results


