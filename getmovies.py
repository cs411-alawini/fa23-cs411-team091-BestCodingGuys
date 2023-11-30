from dotenv import load_dotenv
import os

import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes

load_dotenv()
gcp_project_region_instance = os.getenv("GCP_PROJECT_REGION_INSTANCE")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
# initialize Python Connector object
connector = Connector()
# Python Connector database connection function
def getconn():
    conn = connector.connect(
        gcp_project_region_instance,
        "pymysql",
        user=db_username,
        password=db_password,
        db=db_name,
        ip_type=IPTypes.PUBLIC
    )
    return conn
# Create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

def get_current_movie(movie):
    ret = {"movietitle" : movie,
           "startYear" : 0,
           "runtimeMinutes" : 0
        }
    with pool.connect() as db_conn:
        query = sqlalchemy.text("SELECT primaryTitle, startYear, runtimeMinutes, averageRating, numVotes FROM iMDB_Titles WHERE primaryTitle LIKE :title_input ORDER BY NumVotes DESC LIMIT 20;")
        result = db_conn.execute(query, parameters = {"title_input" : f"%{movie}%"}).fetchall()
        # for row in result:
        #     print(row)
    ret["startYear"] = result[0].startYear
    ret["runtimeMinutes"] = result[0].runtimeMinutes
    return ret

# select primaryTitle, startYear, runtimeMinutes, averageRating, numVotes from iMDB_Titles order by NumVotes desc limit 30;