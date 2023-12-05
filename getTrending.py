# Nathan Created this file. 
import sqlalchemy
from init_database import pool
        
def get_Trending(movie):

    with pool.connect() as db_conn:
        
        query = sqlalchemy.text("SELECT title, VideoId, MAX(TrendingDate) AS TrendingDate, channelTitle, MAX(view_count) AS view_count, DATEDIFF(MAX(TrendingDate), MIN(TrendingDate)) AS days_trending FROM YT_Trending WHERE title LIKE :title_input OR description LIKE :title_input AND (categoryId = '1' OR categoryId = '18' OR categoryId = '23' OR categoryId = '24' OR categoryId = '30' OR categoryId = '31' OR categoryId = '32' OR categoryId = '33' OR categoryId = '34' OR categoryId = '35' OR categoryId = '36' OR categoryId = '37' OR categoryId = '38' OR categoryId = '39' OR categoryId = '40' OR categoryId = '41' OR categoryId = '42' OR categoryId = '43' OR categoryId = '44') GROUP BY title, channelTitle, VideoId ORDER BY MAX(TrendingDate) DESC LIMIT 30;")
        result = db_conn.execute(query, parameters = {"title_input" : f"%{movie}%"}).fetchall()
    return result

# SELECT title, MAX(TrendingDate) AS TrendingDate, channelTitle, MAX(view_count) AS view_count, DATEDIFF(MAX(TrendingDate), MIN(TrendingDate)) AS days_trending FROM YT_Trending WHERE title LIKE :title_input OR description LIKE :title_input AND (categoryId = '1' OR categoryId = '18' OR categoryId = '23' OR categoryId = '24' OR categoryId = '30' OR categoryId = '31' OR categoryId = '32' OR categoryId = '33' OR categoryId = '34' OR categoryId = '35' OR categoryId = '36' OR categoryId = '37' OR categoryId = '38' OR categoryId = '39' OR categoryId = '40' OR categoryId = '41' OR categoryId = '42' OR categoryId = '43' OR categoryId = '44') GROUP BY title, channelTitle ORDER BY MAX(TrendingDate) DESC LIMIT 30;
  