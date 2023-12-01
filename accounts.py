import sqlalchemy
from init_database import pool

def get_current_account(username, password):
    with pool.connect() as db_conn:
        query = sqlalchemy.text("SELECT UserId FROM Users WHERE UserId = :username LIMIT 1;")
        account = db_conn.execute(query, parameters = {"username" : username}).fetchall()
        print(account)
        if len(account) == 0:
            # account does not exist
            print("account does not exist")
            return 0
        
        query = sqlalchemy.text("SELECT UserId, FavMovie FROM Users WHERE UserId = :username AND Password = :password LIMIT 1;")
        account = db_conn.execute(query, parameters = {"username" : username, "password" : password}).fetchall()
        if len(account) == 0:
            # password is incorrect
            print("incorrect password")
            return 1
        
    return account

def create_new_account(username, password, fav_movie):
    with pool.connect() as db_conn:
        create_account_query = sqlalchemy.text("INSERT INTO Users(UserId, Password, FavMovie) VALUES (:username, :password, :fav_movie_id);")
        # need to make a query to search for the title id based on title name, then put that into the insert statement
        db_conn.execute(create_account_query, parameters = {"username" : username, "password" : password, "fav_movie_id" : "tt0903747"})
        db_conn.commit()
    return