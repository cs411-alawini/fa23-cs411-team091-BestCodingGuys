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