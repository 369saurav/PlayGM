import mysql.connector
from mysql.connector import Error

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
            port=4000,
            user="3CHjZydnDAbyLy6.root",
            password="<PASSWORD>",
            database="play_gm",
            ssl_ca="isrgrootx1.pem",
            ssl_verify_cert=True,
            ssl_verify_identity=True
        )
        return connection
    except Error as e:
        print(f"Error connecting to TiDB: {e}")
        return None


def similarity_search(embedding, limit=10):
    global similarity_search_cursor
    connection = get_db_connection()
    results = []
    if connection:
        try:
            similarity_search_cursor = connection.cursor(dictionary=True)

            query = """
                SELECT player_fen, opponent_fen, move_number
                FROM chess_positions
                ORDER BY Vec_Cosine_Distance(embedding, %s)
                LIMIT %s
            """

            similarity_search_cursor.execute(query, (embedding, limit))
            results = similarity_search_cursor.fetchall()

        except Error as error:
            print(f"Error executing query: {error}")
        finally:
            if connection.is_connected():
                similarity_search_cursor.close()
                connection.close()

    return results