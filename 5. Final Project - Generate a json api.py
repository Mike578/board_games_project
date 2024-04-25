from flask import Flask, abort, request, jsonify
import math
import pymysql

app = Flask(__name__)

MAX_PAGE_SIZE = 100

# -----------[PAGE 0]--------------
@app.route("/")
def hello_world():
    return "Hello! \n Welcome to my project. You can type /boardgames to see the list of all the board games and /boardgmaes/id to have more info depending on the id of the board game "


# [GENERAL BOARD GAMES PAGE]
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
                    SELECT bgg_id, name FROM games
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
        'board games': {name: bgg_id for bgg_id, name in sorted(boardgames_with_id.items(), key=lambda x: x[1])},
        'next_page': f'/boardgames?page={page+1}',
        'previous_page': f'/boardgames?page={page-1}',
        'last_page': f'/boardgames?page={last_page}',
    }

    return jsonify(response)

# ----[SUB PAGE : inside a boardgame with given bgg_id] ----
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
                       c.category,
                       s.subcategory,
                       m.mechanism, t.theme
                       FROM games AS g
                       LEFT JOIN mechanics AS m USING(bgg_id)
                       LEFT JOIN themes AS t USING(bgg_id)
                       LEFT JOIN categories AS c USING(bgg_id)
                       LEFT JOIN subcategories AS s USING(bgg_id)
                       WHERE g.bgg_id = %s
        """, (bgg_id, ))
        cursing = cursor.fetchone()
        if not cursing:
            abort(404)

    db_conn.close()

    # Convert the fetched data to JSON and return as a response
    return jsonify(cursing)




# [SUB SUBPAGE: more details for a given bgg_id] :

@app.route("/boardgames/<int:bgg_id>/details")

def details(bgg_id):
    db_conn = pymysql.connect(host="localhost",
                              user="root", 
                              database="bgg",  
                              password="Silver57",
                              cursorclass=pymysql.cursors.DictCursor)

    with db_conn.cursor() as cursor:
        cursor.execute("""
                       SELECT g.bgg_id, g.name, g.description, g.language_ease, g.is_reimplementation_binary, g.kickstarted_binary,
                       a.artist, 
                       d.designer,
                       p.publishing_company
                       FROM games AS g
                       LEFT JOIN artists AS a ON g.bgg_id = a.bgg_id
                       LEFT JOIN designers AS d ON g.bgg_id = d.bgg_id
                       LEFT JOIN publishers AS p ON g.bgg_id = p.bgg_id
                       WHERE g.bgg_id = %s
        """, (bgg_id, ))
        cursing = cursor.fetchone()
        if not cursing:
            abort(404)
            
    db_conn.close()

    # Convert the fetched data to JSON and return as a response
    return jsonify(cursing)


if __name__ == "__main__":
    app.run(debug=True)