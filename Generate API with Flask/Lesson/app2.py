
# [STEP 0: IMPORTING LIBRARIES / FUNCTIONS]


## Many different libraries to import through the exercice / tutorial:

from flask import Flask, abort, request
#abort is used when defining the clean_null + avoiding errors when fetching
# request is used to return all movies with a pagination mechanism

from flask_basicauth import BasicAuth
# BasicAuth is for authentication (ID + Pwd)

import getpass
# BasicAuth is for authentication (ID + Pwd)

import pymysql
#pymysql is for connecting python to MySQL

import os
# os is for the environnment variables --> sql connection / authentication 

import json
# will be used when formating to json/ dct format

from flask_swagger_ui import get_swaggerui_blueprint
# for being able to push the document in a api to to swagger (the place where you can repiblish and people can interact with it)

import math
#maths function

from collections import defaultdict
#It is simply a dictionary but when a key does not exist, 
# it acts as if it were there, with the default value `[]`. 
# So you can always do `the_dict['somekey'].append(something)`.


# --------------------------------------------------------
# --------------------------------------------------------


# ----- [INITIALIZING] ----- 
app = Flask(__name__) #object which refers to our Flask application
app.config.from_file("flask_config.json", load=json.load) #as a json file
auth = BasicAuth(app) #authenticate (ID + pwd) init


# ----- [SETTING THINGS FIRST] -----


# Setting the (My)sql connection:
# NB: if we have to change of sql db, 
# then we should insert it everytime inside each def
db_conn = pymysql.connect(host="localhost",
                          user="root", 
                          database="bechdel",  
                          password = os.getenv('mysqlpass'),
                          #we could also have password = 'your_password'
                          cursorclass=pymysql.cursors.DictCursor)


#setting the pagination
MAX_PAGE_SIZE = 100


#setting the remove null values before anything:
def remove_null_fields(obj):
     return {k:v for k, v in obj.items() if v is not None}


#flask-swagger-ui : I'll come back to it later
swaggerui_blueprint = get_swaggerui_blueprint(
     base_url='/docs',
     api_url='/static/openapi.yaml',
 )
app.register_blueprint(swaggerui_blueprint)




# ----- [DEF FUNCTIONS] -----


# [DEF movie_id]


#declaring routes and authentication security
# @ = a decorator: applies to the function 
# just below/after it and provide it some information
@app.route("/movies/<int:movie_id>") #precising the route + precising that the movie_id is an integer
@auth.required



# --> Let's create our first function: Defining movie_id
def movie(movie_id):

#indide the def_movie, let's first define the cursor
#reminder: cursor = object that we can execute a SQL Query on and that
# will handle data fetching for us

    with db_conn.cursor() as cursor: #defining the cursor
        cursor.execute('''SELECT
                        M.movieId,
                        M.originalTitle,
                        M.primaryTitle AS englishTitle,
                        B.rating AS bechdelScore,
                        M.runtimeMinutes,
                        M.startYear AS Year,
                        M.movieType,
                        M.isAdult
                        FROM Movies M
                        JOIN Bechdel B ON B.movieId = M.movieId 
                        WHERE M.movieId=%s''', (movie_id, ))
        movie = cursor.fetchone()
        if not movie:
            abort(404) #ensure not getting error if we have a null or non existing movie_id
        movie = remove_null_fields(movie) #using the remove_null function we defined sooner
        movie['bechdelTest'] = movie['bechdelScore'] == 3


#Still inthe def movie(movie_id) function, we now focus on the genre:
    with db_conn.cursor() as cursor:
        cursor.execute("SELECT * FROM MoviesGenres WHERE movieId=%s", (movie_id, ))
        genres = cursor.fetchall()
        movie['genres'] = [g['genre'] for g in genres]


#Still in the def movie(movie_id) function, we now focus afterwards on the people:
# defining the 'people' field (actors, realisator, ...):
    with db_conn.cursor() as cursor:
        cursor.execute("""
            SELECT
                P.personId,
                P.primaryName AS name,
                P.birthYear,
                P.deathYear,
                MP.category AS role
            FROM MoviesPeople MP
            JOIN People P on P.personId = MP.personId
            WHERE MP.movieId=%s
        """, (movie_id, ))
        people = cursor.fetchall()
    movie['people'] = [remove_null_fields(p) for p in people]





#ending the def movie(movie_id) function:
    db_conn.close()
    return movie



# '-------


# # --> Let's now dig inside the url by creating our second function: Defining movie_id

# Question 6.1.1: first paginated route 
# + question 6.1.2:  Enhancements to the pagination mechanism

#just as before, let's declare our new route (sub-domain) 
# and keep ensuring we have to autheticate to access the page
@app.route("/movies")   #app.route = declare a route
@auth.required



# [DEF MOVIES()]
def movies(): #defining the function for .../movies


    #URL parameters
    # we have to specify that for the various pages of the website
    # of course, we could have precized this code in the initializing step
    # but better having it inside our def movies() function
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)


#-- (PARENTHESIS / PRECISION)
# we won't do it here as we've already precized it in 
# the initializing, but coud also provide 
# the db_conn (connection setting) for MySQL
#--


# Get the movies
    with db_conn.cursor() as cursor: #defining the cursor "inside" the sql query
        cursor.execute("""
            SELECT * FROM Movies
            ORDER BY movieId
            LIMIT %s
            OFFSET %s
        """, (page_size, (page - 1) * page_size))
        movies = cursor.fetchall()
        movie_ids = [mov['movieId'] for mov in movies]

# defining what the last page would be:
    with db_conn.cursor() as cursor: #defining the cursor again
        cursor.execute("SELECT COUNT(*) AS total FROM Movies")
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)


# [stating the placeholder that will be used for genres and people] (see below)
    placeholder = '%s,' * len(movie_ids)
    placeholder = placeholder[:-1]


# defining the 'genres' field:
    with db_conn.cursor() as cursor:
        cursor.execute(f"""
            SELECT 
                * 
            FROM MoviesGenres 
            WHERE movieId in ({placeholder})
        """, movie_ids)
        genres = cursor.fetchall()
    
    # now looping:
        genres_dict = defaultdict(list)
        for obj in genres:
            movieId = obj['movieId']
            del obj['movieId']
            genres_dict[obj['movieId']].append(obj['genre']) 

    # fetching the movies genre: (comprhension loop)    
    movie['genres'] = [g['genre'] for g in genres]


# defining 'people' field:
    with db_conn.cursor() as cursor:
        
        cursor.execute(f""" SELECT
                            MP.movieId,
                            P.personId,
                            P.primaryName AS name,
                            P.birthYear,
                            P.deathYear,
                            MP.job,
                            MP.category AS role
                        FROM MoviesPeople MP
                        JOIN People P on P.personId = MP.personId
                        WHERE MP.movieId in ({placeholder}) """, movie_ids )
        people = cursor.fetchall()
    
    # now looping:
    people_dict = defaultdict(list)
    for obj in people:
        movieId = obj['movieId']
        del obj['movieId']
        people_dict[movieId].append(obj)


    # X --> Merge genres and people into movies  
    for movie in movies:
        movieId = movie['movieId']
        movie['genres'] = genres_dict[movieId] # adding the genre to each movie_id 'element' 
        movie['people'] = people_dict[movieId] # adding the people (actors, etc...) to each movie_id element

    db_conn.close()

    return {
        'movies': movies,
        'next_page': f'/movies?page={page+1}&page_size={page_size}',
        'last_page': f'/movies?page={last_page}&page_size={page_size}',
        }




