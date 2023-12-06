CREATE TRIGGER AccountCreation
        BEFORE INSERT ON Users
        FOR EACH ROW
        BEGIN
            DECLARE password_length INT;
            DECLARE existing_users INT;
	        DECLARE found_movies INT;
            DECLARE movie_title VARCHAR(255);

	        SELECT COUNT(*) INTO found_movies
	        FROM iMDB_Titles WHERE primaryTitle = NEW.FavMovie;

            SELECT COUNT(*) INTO existing_users
            FROM Users
            WHERE UserId = NEW.UserId;

            SET password_length = CHAR_LENGTH(NEW.Password);
           
	    
            IF existing_users > 1 THEN
                SET @error_message = 'User already exists.';
                SIGNAL SQLSTATE '23000' SET MESSAGE_TEXT = @error_message;
            END IF;

            IF password_length < 8 THEN
                SET @error_message = 'Password does not meet strength requirements';
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = @error_message;
            END IF;

            IF found_movies = 0 THEN
                SET @error_message = 'Movie is not found in the database.';
                SIGNAL SQLSTATE '40000' SET MESSAGE_TEXT = @error_message;
            END IF;
        END;