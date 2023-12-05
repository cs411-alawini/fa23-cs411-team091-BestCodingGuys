CREATE TRIGGER CheckPasswordStrength
        BEFORE INSERT ON Users
        FOR EACH ROW
        BEGIN
            DECLARE password_length INT;
            DECLARE existing_users INT;
            
            SELECT COUNT(*) INTO existing_users
            FROM Users
            WHERE UserID = New.UserID;

            SET password_length = CHAR_LENGTH(NEW.Password);
            
            IF existing_users > 1 THEN
                SET @error_message = 'User already exists.';
                SIGNAL SQLSTATE '23000' SET MESSAGE_TEXT = @error_message;
            END IF;

            IF password_length < 8 THEN
                SET @error_message = 'Password does not meet strength requirements';
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = @error_message;
            END IF;
        END;