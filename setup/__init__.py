from operator import index

import requests
from bs4 import BeautifulSoup
import chess
import chess.pgn
import io
import mysql.connector
from flask import jsonify
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup
import time
import random
import json
import re
from datetime import datetime
from mysql.connector import Error

from app import create_table
from main import embedding
import os
from tidb_vector.integrations import TiDBVectorClient
from dotenv import load_dotenv


# # Function to scrape PGN data from a website
def scrape_pgn_data(url):
    global last_record_cursor
    start = 0
    last_record_inserted_data_query = """
        SELECT
          last_record_inserted
        FROM
          `chess_365_data_status`
        WHERE id = 1;"""
    connection = get_db_connection()
    if connection:
        try:
            last_record_cursor = connection.cursor()
            last_record_cursor.execute(last_record_inserted_data_query)
            fetched_result = last_record_cursor.fetchone()

            if fetched_result:
                start = fetched_result[0]  # Assuming last_record_inserted is the first (and only) column
            else:
                start = 0  # Or some default value if no record is found            start = last_record_cursor.execute(last_record_inserted_data_query)

            print("start::: "+str(start))

        except mysql.connector.Error as error:
            print(f"Error fetching chess_365_data_status table: {error}")
        finally:
            if connection.is_connected():
                last_record_cursor.close()

    end = 3520
    row_counter = start
    for page in range (start, end):
        new_url = url+str(start)
        print("new_url::  "+new_url)
        response = requests.get(new_url)

        print(response.status_code)
        main_page_soup = BeautifulSoup(response.text, 'html.parser')

        div_mainfull = main_page_soup.find('div', id='mainfull')
        table = div_mainfull.find('table', class_='table stable')
        tbody = table.find('tbody')
        tr_list = tbody.findAll('tr')
        pgn_data_list = []
        counter = 1
        for tr in tr_list:
            td_list = tr.findAll('td')

            print("td_list size :::"+str(len(td_list)))
            td = td_list[9]
            a = td.find('a')
            href = a.attrs
            print(str(href))
            on_click_tag = href["onclick"]
            url_pattern = r"ajaxPopup\('([^']+)'"
            match = re.search(url_pattern, on_click_tag)
            extracted_url = ''
            if match:
                extracted_url = match.group(1)
                print("Extracted URL:", extracted_url)
            else:
                print("No URL found.")
            pgn_page = requests.get(extracted_url)
            print(pgn_page.status_code)
            pgn_page_soap = BeautifulSoup(pgn_page.text, 'html.parser')
            # print("pgn_page::: "+str(pgn_page_soap.prettify()))
            pgn = pgn_page_soap.find('div', id='GameTextLayerPopup').text
            sidebar_table_data_list = pgn_page_soap.find('div', id='sidebar2').find('table').findAll('tr')


            white_name = ''
            white_rating = None
            black_name = ''
            black_rating = None
            event_name = ''
            site_name = ''
            date_str = ''
            eco_code = ''
            score = ''

            for tr_data in sidebar_table_data_list:
                if sidebar_table_data_list.index(tr_data) == 0:
                    print("tr_data (0)::: "+str(tr_data))
                elif sidebar_table_data_list.index(tr_data) == 1:
                    name_pattern = r'middle">\s*([^<]+?)\s*<em>'
                    rating_pattern = r'<em>\((\d+)\)</em>'

                    # Search the patterns in the tr_data string
                    match_name = re.search(name_pattern, str(tr_data))
                    match_rating = re.search(rating_pattern, str(tr_data))



                    if match_name:
                        white_name = match_name.group(1).strip()
                    else:
                        print("No name found.")

                    if match_rating:
                        white_rating = int(match_rating.group(1).strip())
                    else:
                        print("No rating found.")

                    print("white_name :",white_name)
                    print("white_rating :", white_rating)
                    print("tr_data (1)::: " + str(tr_data))

                elif sidebar_table_data_list.index(tr_data) == 2:
                    print("tr_data (2)::: "+str(tr_data))
                elif sidebar_table_data_list.index(tr_data) == 3:
                    name_pattern = r'middle">\s*([^<]+?)\s*<em>'
                    rating_pattern = r'<em>\((\d+)\)</em>'

                    # Search the patterns in the tr_data string
                    match_name = re.search(name_pattern, str(tr_data))
                    match_rating = re.search(rating_pattern, str(tr_data))



                    if match_name:
                        black_name = match_name.group(1).strip()
                    else:
                        print("No name found.")

                    if match_rating:
                        black_rating = int(match_rating.group(1).strip())
                    else:
                        print("No rating found.")

                    print("black_name :", black_name)
                    print("black_rating :", black_rating)
                    print("tr_data (3)::: " + str(tr_data))

                elif sidebar_table_data_list.index(tr_data) == 4:
                    event_pattern = r'Event:\s*(.*?)\s*</td>'
                    # Search for the pattern in the tr_data string
                    match_event = re.search(event_pattern, str(tr_data))



                    if match_event:
                        event_name = match_event.group(1).strip()
                    else:
                        print("No event name found.")

                    print("event_name :", event_name)
                    print("tr_data (4)::: " + str(tr_data))

                elif sidebar_table_data_list.index(tr_data) == 5:
                    site_pattern = r'Site:\s*(.*?)\s*</td>'

                    # Search for the pattern in the tr_data string
                    match_site = re.search(site_pattern, str(tr_data))


                    if match_site:
                        site_name = match_site.group(1).strip()
                    else:
                        print("No site name found.")

                    print("site_name :", site_name)
                    print("tr_data (5)::: " + str(tr_data))

                elif sidebar_table_data_list.index(tr_data) == 6:
                    date_pattern = r'Date:\s*(\d{2}/\d{2}/\d{4})'

                    # Search for the pattern in the tr_data string
                    match_date = re.search(date_pattern, str(tr_data))


                    if match_date:
                        date_str = match_date.group(1).strip()

                    else:
                       print('No date found.')

                    print("date :", date_str)
                    print("tr_data (6)::: " + str(tr_data))
                elif sidebar_table_data_list.index(tr_data) == 7:
                    eco_pattern = r'ECO:\s*([^\s<]+)'
                    score_pattern = r'Score:\s*([\d-]+)'

                    # Search for the patterns in the tr_data string
                    match_eco = re.search(eco_pattern, str(tr_data))
                    match_score = re.search(score_pattern, str(tr_data))



                    if match_eco:
                        eco_code = match_eco.group(1).strip()
                    else:
                        print("No ECO code found.")

                    if match_score:
                        score = match_score.group(1).strip()
                    else:
                        print("No score found.")

                    print("eco_code :", eco_code)
                    print("score :", score)
                    print("tr_data (7)::: " + str(tr_data))



            print("eco::: "+str(sidebar_table_data_list))
            print("pgn::: "+str(pgn))
            pgn_data_list.append(pgn)
            print(pgn_data_list)
            fen_list = pgn_to_fen_positions(pgn)
            player_name = ''
            opponent_name = ''
            player_color=''
            player_rating=None
            opponent_rating=None
            result=''
            if white_name == "Carlsen, Magnus":
                player_name = white_name
                opponent_name = black_name
                player_color = 'W'
                player_rating = white_rating
                opponent_rating = black_rating
                if score == '0-1':
                    result = 'L'
                elif score == '1-0':
                    result = 'W'
                else:
                    result='D'
            else:
                player_name = black_name
                opponent_name = white_name
                player_color = 'B'
                player_rating = black_rating
                opponent_rating = white_rating
                if score == '1-0':
                    result = 'L'
                elif score == '0-1':
                    result = 'W'
                else:
                    result='D'
            print("player_name::: "+player_name+" : "+player_color+" : "+result)
            store_in_database(player_name,player_rating,opponent_rating,opponent_name,date_str,player_color,pgn,event_name,eco_code,site_name,fen_list,result,row_counter,new_url,extracted_url)
            print("Counter::: "+str(counter))
            counter+=1
            print("row_counter::: "+str(row_counter))
            row_counter+=1

        start+=40
        print("page_no::: "+str(start/40))


    return None


# Function to convert PGN to FEN positions
def pgn_to_fen_positions(pgn_string):
    game = chess.pgn.read_game(io.StringIO(pgn_string))
    board = game.board()
    positions = []
    for move in game.mainline_moves():
        board.push(move)
        positions.append(board.fen())
    print(positions)
    return positions


# Function to generate embedding for a FEN position
def generate_embedding(fen):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    generated_embedding = model.encode(fen)
    return generated_embedding.tolist()  # Convert numpy array to list

    #         white_name = ''
    #         white_rating = None
    #         black_name = ''
    #         black_rating = None
    #         event_name = ''
    #         site_name = ''
    #         date_str = ''


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
            port=4000,
            user="3CHjZydnDAbyLy6.root",
            password="LJIBsOyh00RIQLC0",
            database="play_gm",
            ssl_ca="isrgrootx1.pem",
            ssl_verify_cert=True,
            ssl_verify_identity=True
        )
        return connection
    except Error as e:
        print(f"Error connecting to TiDB: {e}")
        return None

# Function to store data in the database
def store_in_database(player_name, player_rating, opponent_rating, opponent_name, date, player_color, pgn, event, eco, location, positions, result, chess_365_row_number, last_record_page_url, last_record_pgn_url):
    global cursor
    print("store_in_database::: ")
    print(f"Player Name: {player_name}")
    print(f"Player Rating: {player_rating}")
    print(f"Opponent Rating: {opponent_rating}")
    print(f"Opponent Name: {opponent_name}")
    print(f"Date: {date}")
    print(f"Player Color: {player_color}")
    print(f"PGN: {pgn}")
    print(f"Event: {event}")
    print(f"ECO: {eco}")
    print(f"Location: {location}")
    print(f"Positions: {positions}")
    print(f"Result: {result}")
    try:
        # Convert to datetime object
        date_obj = datetime.strptime(date, '%m/%d/%Y')
        formatted_date = date_obj.strftime('%Y-%m-%d')  # Format as YYYY-MM-DD
    except ValueError:
        print('ERROR: Invalid date format')
        return None
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Insert game data
            cursor.execute("""
               INSERT INTO chess_games_data 
               (player_name, player_rating, opponent_name, opponent_rating, date, player_piece_color, chess_annotation_pgn, ECO, result, event, location)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               """, (
            player_name, player_rating, opponent_name, opponent_rating, formatted_date, player_color, pgn, eco, result, event,
            location))
            game_id = cursor.lastrowid
            print("game_id::: "+str(game_id))
            print("positions::: "+str(positions))
            # Insert position data
            for_counter = 0
            for i ,fen in enumerate(positions):
                players_fen = ''
                opponent_fen = ''
                fen_embedding = ''
                for_counter += 1
                print("i::: "+str(i))
                if player_color == 'W':
                    if i%2 == 0:
                        if i == 0:
                            opponent_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
                            players_fen = str(fen)
                            fen_embedding = str(generate_embedding(opponent_fen))
                        else:
                            continue
                    else:
                        # "blacks move"
                        if len(positions) == i+1:
                            players_fen = ''
                            opponent_fen = str(fen)
                            fen_embedding = str(generate_embedding(opponent_fen))
                        else:
                            opponent_fen = str(fen)
                            players_fen = str(positions[i+1])
                            fen_embedding = str(generate_embedding(opponent_fen))

                elif player_color == 'B':
                    if i%2 == 0:
                        # "whites move"
                        if len(positions) == i+1:
                            players_fen = ''
                            opponent_fen = str(fen)
                            fen_embedding = str(generate_embedding(opponent_fen))
                        else:
                            opponent_fen = str(fen)
                            players_fen = str(positions[i+1])
                            fen_embedding = str(generate_embedding(opponent_fen))
                    else:
                        continue

                # print("for_counter::: "+str(for_counter))
                print("fen_embedding::: "+str(fen_embedding))
                cursor.execute("""
                   INSERT INTO `chess_positions` (`game_id`,`player_color`,`player_fen`,`opponent_fen`,`move_number`,`embedding`) VALUES (%s, %s, %s, %s, %s, %s)

                   """, (game_id,player_color, players_fen, opponent_fen, i + 1, str(fen_embedding)))

            update_chess_365_status_query = """
            UPDATE `chess_365_data_status`
            SET
              `last_record_inserted` = %s, `last_record_page_url` = %s, `last_record_pgn_url` = %s WHERE `id` = 1"""
            cursor.execute(update_chess_365_status_query,(chess_365_row_number,last_record_page_url,last_record_pgn_url))
            connection.commit()

        except mysql.connector.Error as error:
            print(f"Error creating table: {error}")
        finally:
            if connection.is_connected():
                cursor.close()



    # conn.commit()
    # conn.close()

# Main process
def main():
    url = "https://www.365chess.com/players/Magnus_Carlsen/?p=1&start="  # Replace with actual URL
    # scrape_pgn_data(url)
    pgn_data_list = scrape_pgn_data(url)
    # fen_positions = pgn_to_fen_positions(pgn_data)
    #
    # # Extract metadata from PGN (this is a simplification, you'll need to parse the PGN header)
    # player_name = "Carlsen, Magnus"
    # opponent_name = "Opponent Name"
    # game_date = "2024-05-30"
    # player_color = "white"  # or "black"
    #
    # store_in_database(player_name, opponent_name, game_date, player_color, pgn_data, fen_positions)


if __name__ == "__main__":
    main()