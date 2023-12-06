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
        
        try:
            create_account_query = sqlalchemy.text("INSERT INTO Users(UserId, Password, FavMovie) VALUES (:username, :password, :fav_movie);")
            # need to make a query to search for the title id based on title name, then put that into the insert statement
            db_conn.execute(create_account_query, parameters = {"username" : username, "password" : password, "fav_movie" : fav_movie})
            db_conn.commit()
        except sqlalchemy.exc.IntegrityError as e:
            #Throws error if insertion of pre-existing username is attempted.
            print("username error")
            print(str(e))
            db_conn.rollback()
            return 1
        except sqlalchemy.exc.DatabaseError as e:
            #Throws error if insertion of password not meeting strength requirements is attempted.
            if 'Password does not meet strength requirements' in str(e):
               print("weak password")
               print(str(e))
               db_conn.rollback()
               return 2
            #Throws error if insertion of movie is not found in the database
            if 'Movie is not found in the database.' in str(e):
               print("missing movie")
               print(str(e))
               db_conn.rollback()
               return 3

def update_account(selected_movie, user_id):
    with pool.connect() as db_conn:
        print("updating ", user_id, " to FavMovie ", selected_movie)
        query = sqlalchemy.text("UPDATE Users SET FavMovie = :movie WHERE UserId = :user_id;")
        db_conn.execute(query, parameters = {"movie" : selected_movie.primaryTitle, "user_id" : user_id})
        db_conn.commit()
        return