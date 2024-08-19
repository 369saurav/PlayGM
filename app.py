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

# Create table if not exists
def create_table():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            create_table_query = """
                   CREATE TABLE IF NOT EXISTS chess_games (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       player_name VARCHAR(100) NOT NULL,
                       opponent_name VARCHAR(100) NOT NULL,
                       game_date DATE NOT NULL,
                       player_piece_color ENUM('white', 'black') NOT NULL,
                       chess_annotation TEXT NOT NULL,
                       embedding VECTOR(384)
                   );
                   """
            # create_index_query = "CREATE INDEX idx_items_embedding ON chess_games USING ann(embedding) WITH (dimensions=384, distance_metric='cosine');"
            cursor.execute(create_table_query)
            # cursor.execute(create_index_query)
            connection.commit()
            print("Table 'chess_games' created successfully")
        except mysql.connector.Error as error:
            print(f"Error creating table: {error}")
        finally:
            if connection.is_connected():
                cursor.close()

# create_table()

# API Routes
@app.route('/chess/embedding', methods=['POST'])
def create_employee():
    data = request.json
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO chess_games (player_name, opponent_name, game_date, player_piece_color, chess_annotation, embedding) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (data['player_name'], data['opponent_name'], data['game_date'], data['player_piece_color'], data['chess_annotation'], data['embedding'])
            cursor.execute(sql, values)
            connection.commit()
            return jsonify({"message": "Employee created successfully", "id": cursor.lastrowid}), 201
        except Error as e:
            return jsonify({"error": str(e)}), 400
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return jsonify({"error": "Database connection failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)