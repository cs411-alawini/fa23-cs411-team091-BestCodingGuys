import sqlalchemy
from init_database import pool

def get_current_movie(movie):

    with pool.connect() as db_conn:
        query = sqlalchemy.text("SELECT primaryTitle, startYear, runtimeMinutes, averageRating, numVotes FROM iMDB_Titles WHERE primaryTitle LIKE :title_input ORDER BY NumVotes DESC LIMIT 20;")
        result = db_conn.execute(query, parameters = {"title_input" : f"%{movie}%"}).fetchall()

    return result

# select primaryTitle, startYear, runtimeMinutes, averageRating, numVotes from iMDB_Titles order by NumVotes desc limit 30;