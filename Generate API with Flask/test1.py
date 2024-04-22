from flask import Flask
import json
import math
import pymysql
from collections import defaultdict
from flask import Flask, abort, request
from flask_basicauth import BasicAuth
from flask_swagger_ui import get_swaggerui_blueprint
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

def remove_null_fields(obj):
    return {k:v for k, v in obj.items() if v is not None}


MAX_PAGE_SIZE = 50



@app.route("/")
def hello_world():
    return "Hello!"


# ---- first page----
@app.route("/character")
def characters():
    page = int(request.args.get('page', 0))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)
    include_details = bool(int(request.args.get('include_details', 0)))
    
    db_conn = pymysql.connect(host="localhost",
                            user="root", 
                            database="GOT",  
                            password = "Silver57",
                            cursorclass=pymysql.cursors.DictCursor)

    # Get character
    with db_conn.cursor() as cursor:
        cursor.execute("""
                    select name, house from predictions 
                    order by name 
                    LIMIT %s
                    OFFSET %s; 
                    """ , (page_size, page * page_size))
        character = cursor.fetchall()
        character_ = [char['name'] for char in character]

    with db_conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM predictions")
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)
    db_conn.close()
    return {
        'character': character,
        'next_page': f'/character?page={page+1}&page_size={page_size}&include_details={int(include_details)}',
        'last_page': f'/character?page={last_page}&page_size={page_size}&include_details={int(include_details)}',
    }




#---next page----
@app.route("/character/<int:character_id>")
def character(character_id):
    
    db_conn = pymysql.connect(host="localhost",
                            user="root", 
                            database="GOT",  
                            password = "Silver57",
                            cursorclass=pymysql.cursors.DictCursor)


    with db_conn.cursor() as cursor:
        cursor.execute("""
select p.character_id, p.name, p.father, p.mother, p.house,  d.gender, d.death_chapter, d.book_of_death, p.DateoFdeath,
CASE 
WHEN p.DateoFdeath is null
then 'Alive'
else 'Dead'
end as dead_or_not
from predictions as p
left join death2 as d
	on p.name = d.name
            WHERE p.character_id = %s
        """, (character_id, ))
        charac = cursor.fetchone()
        if not charac:
            abort(404)
        charac = remove_null_fields(charac)
            
    db_conn.close()
    return charac

@app.route("/character/details")
def details():
    page = int(request.args.get('page', 0))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)
    include_details = bool(int(request.args.get('include_details', 0)))
    
    db_conn = pymysql.connect(host="localhost",
                            user="root", 
                            database="GOT",  
                            password = "Silver57",
                            cursorclass=pymysql.cursors.DictCursor)

    # Get character
    with db_conn.cursor() as cursor:
        cursor.execute("""
select p.character_id, p.name, p.father, p.mother, p.house,  d.gender, d.death_chapter, d.book_of_death, p.DateoFdeath,
CASE 
WHEN p.DateoFdeath is null
then 'Alive'
else 'Dead'
end as dead_or_not
from predictions as p
left join death2 as d
	on p.name = d.name
                    LIMIT %s
                    OFFSET %s; 
                    """ , (page_size, page * page_size))
        character = cursor.fetchall()
        character_ = [char['name'] for char in character]

        

    with db_conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM predictions")
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)
    db_conn.close()
    return {
        'character': character,
        'next_page': f'/character?page={page+1}&page_size={page_size}&include_details={int(include_details)}',
        'last_page': f'/character?page={last_page}&page_size={page_size}&include_details={int(include_details)}',
    }