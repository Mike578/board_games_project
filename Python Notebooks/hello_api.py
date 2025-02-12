from flask import Flask, request, jsonify
import pymysql
import os
import math
import getpass

app = Flask(__name__)

MAX_PAGE_SIZE = 100

# Demander le mot de passe MySQL de manière sécurisée
password = getpass.getpass("Entrez votre mot de passe MySQL : ")

def get_db_connection():
    """Établit une connexion à la base de données MySQL."""
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        database="bgg_project",
        password=password,
        cursorclass=pymysql.cursors.DictCursor
    )


# -----------[PAGE 0]--------------
@app.route("/")
def hello_world():
    return (
        "Hello! \n Welcome to my project. You can type /boardgames to see "
        "the list of all the board games and /boardgames/id to have more info "
        "depending on the id of the board game"
    )


# [GENERAL BOARD GAMES PAGE]
@app.route("/boardgames")
def boardgames():
    page = int(request.args.get('page', 0))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)

    db_conn = get_db_connection()
    if not db_conn:
        return jsonify({"error": "Impossible de se connecter à la base de données"}), 500

    try:
        with db_conn.cursor() as cursor:
            cursor.execute("""
                SELECT bgg_id, name 
                FROM df_games_before_cleaning
                ORDER BY bgg_id 
                LIMIT %s OFFSET %s;
            """, (page_size, page * page_size))
            boardgames = cursor.fetchall()

            # Correction : utiliser bgg_id comme clé pour éviter les pertes de données
            boardgames_with_id = {bg['bgg_id']: bg['name'] for bg in boardgames}

        with db_conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM df_games_before_cleaning")
            boardy = cursor.fetchone()
            last_page = math.ceil(boardy['total'] / page_size)

        response = {
            'board games': boardgames_with_id,
            'next_page': f'/boardgames?page={page+1}' if page + 1 < last_page else None,
            'previous_page': f'/boardgames?page={page-1}' if page > 0 else None,
            'last_page': f'/boardgames?page={last_page-1}'
        }

        return jsonify(response)
    
    finally:
        db_conn.close()


# [BOARD GAME DETAILS PAGE]
@app.route("/boardgames/<int:bgg_id>")
def boardgame_details(bgg_id):
    """Retourne les détails d'un jeu de société en fonction de son bgg_id."""
    
    db_conn = get_db_connection()
    if not db_conn:
        return jsonify({"error": "Impossible de se connecter à la base de données"}), 500

    try:
        with db_conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    g.bgg_id,
                    g.name,
                    g.year_published,
                    ROUND(g.avg_rating, 2) AS average_rating,
                    ROUND(g.game_weight, 1) AS game_difficulty,
                    rd.total_ratings,
                    g.mfg_age_rec AS manufacturer_age_reco,
                    ROUND(g.com_age_rec, 0) AS community_age_reco,
                    g.mfg_playtime AS manufacturer_playtime_reco,
                    g.com_min_playtime AS community_min_playtime,
                    g.com_max_playtime AS community_max_playtime,
                    ti.theme,
                    mi.mechanic,
                    ai.artists,
                    pi.publisher
                FROM bgg_project.df_games_before_cleaning AS g 
                LEFT JOIN bgg_project.mechanics_improved AS mi USING (bgg_id)
                LEFT JOIN bgg_project.artists_improved AS ai USING (bgg_id)
                LEFT JOIN bgg_project.publishers_improved AS pi USING (bgg_id)
                LEFT JOIN bgg_project.themes_improved AS ti USING (bgg_id)
                LEFT JOIN bgg_project.ratings_distribution AS rd USING (bgg_id)
                WHERE g.bgg_id = %s;
            """, (bgg_id,))
            game_details = cursor.fetchone()

            if not game_details:
                return jsonify({"error": f"Aucun jeu trouvé avec le bgg_id {bgg_id}"}), 404

        return jsonify(game_details)
    
    except pymysql.MySQLError as e:
        return jsonify({"error": f"Erreur SQL : {str(e)}"}), 500
    
    finally:
        db_conn.close()



# [BOARD GAME DETAILS PAGE]
@app.route("/boardgames/<int:bgg_id>/details")
def boardgame_full_details(bgg_id):
    """Retourne les détails complets d'un jeu de société en fonction de son bgg_id."""
    
    db_conn = get_db_connection()
    if not db_conn:
        return jsonify({"error": "Impossible de se connecter à la base de données"}), 500

    try:
        with db_conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    g.bgg_id,
                    g.name,
                    g.mfg_age_rec AS manufacturer_age_reco,
                    ROUND(g.com_age_rec, 0) AS community_age_reco,
                    g.mfg_playtime AS manufacturer_playtime_reco,
                    g.com_min_playtime AS community_min_playtime,
                    g.com_max_playtime AS community_max_playtime,
                    ti.theme,
                    mi.mechanic,
                    ai.artists,
                    pi.publisher,
                    g.kickstarted,
                    g.description,
                    g.image_path
                FROM bgg_project.df_games_before_cleaning AS g 
                LEFT JOIN bgg_project.mechanics_improved AS mi USING (bgg_id)
                LEFT JOIN bgg_project.artists_improved AS ai USING (bgg_id)
                LEFT JOIN bgg_project.publishers_improved AS pi USING (bgg_id)
                LEFT JOIN bgg_project.themes_improved AS ti USING (bgg_id)
                LEFT JOIN bgg_project.ratings_distribution AS rd USING (bgg_id)
                WHERE g.bgg_id = %s;
            """, (bgg_id,))
            game_details = cursor.fetchone()

            if not game_details:
                return jsonify({"error": f"Aucun jeu trouvé avec le bgg_id {bgg_id}"}), 404

        return jsonify(game_details)
    
    except pymysql.MySQLError as e:
        return jsonify({"error": f"Erreur SQL : {str(e)}"}), 500
    
    finally:
        db_conn.close()


if __name__ == "__main__":
    app.run(debug=True, port=8080)



@app.route("/boardgames/kickstarted")
def kickstarted_boardgames():
    """Retourne la liste paginée des jeux financés sur Kickstarter avec leurs informations clés."""
    
    page = int(request.args.get('page', 0))  # Page par défaut = 0
    page_size = int(request.args.get('page_size', 100))  # Max 100 jeux par page
    page_size = min(page_size, 100)  # Ne pas dépasser 100

    db_conn = get_db_connection()
    if not db_conn:
        return jsonify({"error": "Impossible de se connecter à la base de données"}), 500

    try:
        with db_conn.cursor() as cursor:
            # Récupération des jeux pour la page demandée
            cursor.execute("""
                SELECT 
                    bgg_id, 
                    name, 
                    year_published, 
                    num_expansions, 
                    num_implementations
                FROM bgg_project.df_games_before_cleaning
                WHERE kickstarted = 1
                ORDER BY year_published DESC
                LIMIT %s OFFSET %s;
            """, (page_size, page * page_size))
            kickstarted_games = cursor.fetchall()

            # Récupération du nombre total de jeux financés sur Kickstarter
            cursor.execute("SELECT COUNT(*) AS total FROM bgg_project.df_games_before_cleaning WHERE kickstarted = 1")
            total_games = cursor.fetchone()['total']
            last_page = total_games // page_size

        # Construction de la réponse JSON avec pagination
        response = {
            'total': total_games,
            'kickstarted_games': kickstarted_games,
            'next_page': f'/boardgames/kickstarted?page={page+1}&page_size={page_size}' if (page + 1) * page_size < total_games else None,
            'previous_page': f'/boardgames/kickstarted?page={page-1}&page_size={page_size}' if page > 0 else None,
            'last_page': f'/boardgames/kickstarted?page={last_page}&page_size={page_size}'
        }

        return jsonify(response)

    except pymysql.MySQLError as e:
        return jsonify({"error": f"Erreur SQL : {str(e)}"}), 500

    finally:
        db_conn.close()




# Lancer l'application Flask
if __name__ == "__main__":
    app.run(debug=True, port=8080)