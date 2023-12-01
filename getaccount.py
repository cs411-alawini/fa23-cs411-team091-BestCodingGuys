import sqlalchemy
from init_database import pool

def get_current_account(username, password):
    with pool.connect() as db_conn:
        query = sqlalchemy.text("SELECT UserId, FavMovie FROM Users WHERE UserId = :username AND Password = :password LIMIT 1;")
        account = db_conn.execute(query, parameters = {"username" : username, "password" : password}).fetchall()
    if len(account) == 0:
        account = {"UserId" : "account not in db", "FavMovie" : "account not in db"}
    return account
