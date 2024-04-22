from flask import Flask, abort, request, jsonify
import json
import math
import pymysql
from collections import defaultdict

app = Flask(__name__)

MAX_PAGE_SIZE = 100

@app.route("/")
def hello_world():
    return "Hello! Welcome to my project. You can type /boardgames to see the list of all the board games and /boardgmaes/id to have more info depending on the id of the board game "

@app.route("/boardgames")
def boardgames():
    page = int(request.args.get('page', 0))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)
    include_details = bool(int(request.args.get('include_details', 0)))

    db_conn = pymysql.connect(host="localhost",
                              user="root", 
                              database="bgg",  
                              password="Silver57",
                              cursorclass=pymysql.cursors.DictCursor)

    # Get boardgames
    with db_conn.cursor() as cursor:
        cursor.execute("""
                    SELECT g.bgg_id, g.name FROM games AS g
                    ORDER BY bgg_id 
                    LIMIT %s
                    OFFSET %s; 
                    """, (page_size, page * page_size))
        boardgames = cursor.fetchall()
        boardgames_with_id = {bg['name']: bg['bgg_id'] for bg in boardgames}

    with db_conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM games")
        boardy = cursor.fetchone()
        last_page = math.ceil(boardy['total'] / page_size)
    db_conn.close()
    
    # Format the response to include both game name and ID
    response = {
        'board games': {name: f"{name} : {bgg_id}" for name, bgg_id in boardgames_with_id.items()},
        'next_page': f'/boardgames?page={page+1}&page_size={page_size}&include_details={int(include_details)}',
        'last_page': f'/boardgames?page={last_page}&page_size={page_size}&include_details={int(include_details)}',
    }
    
    return response


# ----inside a boardgame with given bgg_id----

@app.route("/boardgames/<int:bgg_id>")
def bgg(bgg_id):
    db_conn = pymysql.connect(host="localhost",
                              user="root", 
                              database="bgg",  
                              password="Silver57",
                              cursorclass=pymysql.cursors.DictCursor)

    with db_conn.cursor() as cursor:
        cursor.execute("""
                       SELECT g.bgg_id, g.name, g.year_published, 
                       g.game_difficulty, g.avg_rating, g.min_players, g.max_players, g.com_age_rec,
                       m.mechanism, t.theme 
                       FROM games AS g
                       LEFT JOIN mechanics AS m ON g.bgg_id = m.bgg_id
                       LEFT JOIN themes AS t ON g.bgg_id = t.bgg_id
                       WHERE g.bgg_id = %s
        """, (bgg_id, ))
        boardid = cursor.fetchone()
        if not boardid:
            abort(404)
            
    db_conn.close()
    
    # Convert the fetched data to JSON and return as a response
    return jsonify(boardid)

if __name__ == "__main__":
    app.run(debug=True)
