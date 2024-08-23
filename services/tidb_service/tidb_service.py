import mysql.connector
from mysql.connector import Error
from sympy import partition


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


def similarity_search(embedding, player_name, limit=5):
    global similarity_search_cursor
    connection = get_db_connection()
    results = []
    partition_name = "p" + str(get_player_id(player_name))
    print(str(partition_name))
    if connection:
        try:
            similarity_search_cursor = connection.cursor(dictionary=True)

            # Correct query string with formatted partition name and placeholders for parameters
            query = f"""
                SELECT player_fen, opponent_fen, move_number
                FROM chess_positions PARTITION ({partition_name})
                ORDER BY Vec_Cosine_Distance(embedding, %s)
                LIMIT %s
            """

            # Use the embedding and limit as parameters
            similarity_search_cursor.execute(query, (embedding, limit))
            results = similarity_search_cursor.fetchall()

        except Error as error:
            print(f"Error executing query: {error}")
        finally:
            if connection.is_connected():
                similarity_search_cursor.close()
                connection.close()

    return results


def get_all_players():
    global get_all_players_cursor
    connection = get_db_connection()
    results = []
    if connection:
        try:
            get_all_players_cursor = connection.cursor(dictionary=True)

            query = """
                   SELECT player_name, player_display_name
                   FROM chess_players
               """

            get_all_players_cursor.execute(query)
            results = get_all_players_cursor.fetchall()

        except Error as error:
            print(f"Error executing query: {error}")
        finally:
            if connection.is_connected():
                get_all_players_cursor.close()
                connection.close()

    return results

def get_player_id(player_name):
    connection = None
    cursor = None
    result = None
    try:
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT id FROM chess_players WHERE player_name = %s"
            cursor.execute(query, (player_name,))
            result = cursor.fetchone()
    except Error as error:
        print(f"Error executing query: {error}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
    return result['id'] if result else None

