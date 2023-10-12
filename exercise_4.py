import pymysql


class Exercise4(object):
    def __init__(self):
        # Connect to the MYSQL
        self.conn = pymysql.connect(
            host="127.0.0.1",  
            port=3306,       
            user="root",     
            password="root",   
            database="exercise",   
            charset="utf8"    
        )

        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

        # Create table
        create_book_sql = """
        CREATE TABLE IF NOT EXISTS Books (
            BookID VARCHAR(20) PRIMARY KEY,
            Title TEXT,
            Author TEXT,
            ISBN TEXT,
            Status TEXT
        );
        """
        create_user_sql = """
        CREATE TABLE IF NOT EXISTS Users (
            UserID VARCHAR(20) PRIMARY KEY,
            Name TEXT,
            Email TEXT
        );
        """
        create_reservations_sql = """
        CREATE TABLE IF NOT EXISTS Reservations (
            ReservationID VARCHAR(20) PRIMARY KEY,
            BookID VARCHAR(20),
            UserID VARCHAR(20),
            ReservationDate DATE,
            FOREIGN KEY (BookID) REFERENCES Books (BookID),
            FOREIGN KEY (UserID) REFERENCES Users (UserID)
        );
        """
        self.cursor.execute(create_book_sql)
        self.cursor.execute(create_user_sql)
        self.cursor.execute(create_reservations_sql)

    def insert_sql(self, sql, data):
        # write data to mysql
        self.cursor.execute(sql, tuple(data))
        self.conn.commit()

    def deal(self):
        self.insert_sql(
            "INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (%s, %s, %s, %s, %s)",
            ["LB01", "TestBookTitle1", "TestAuthor1", "VSAJSIW01", "1"]
        )
        self.insert_sql(
            "INSERT INTO Users (UserID, Name, Email) VALUES (%s, %s, %s)",
            ["LU01", "UserName01", "TestEmail@outlook.com"]
        )
        self.insert_sql(
            "INSERT INTO Reservations (ReservationID, BookID, UserID, ReservationDate) VALUES (%s, %s, %s, %s)",
            ["LR01", "LB01", "LU01", "2023/09/27 11:08"]
        )

        self.cursor.execute("""SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status, 
                        Users.Name, Users.Email, Reservations.ReservationDate 
                        FROM Books 
                        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                        LEFT JOIN Users ON Users.UserID = Reservations.UserID
                        WHERE Books.BookID = %s""", ("LB01",))
        book_details = self.cursor.fetchone()
        if book_details:
            book_details = list(book_details.values())
            print("Book Details:")
            print("BookID:", book_details[0])
            print("Title:", book_details[1])
            print("Author:", book_details[2])
            print("ISBN:", book_details[3])
            print("Status:", book_details[4])
            
            if book_details[5]:
                print("Reserved by:")
                print("Name:", book_details[5])
                print("Email:", book_details[6])
                print("Reservation Date:", book_details[7])
        else:
            print("Book not found.")

        input_text = input("Searh Key:")

        if input_text.startswith("LB"):
            self.cursor.execute("""SELECT Books.Status 
                            FROM Books 
                            WHERE Books.BookID = %s""", (input_text,))
            status = self.cursor.fetchone()
            if status:
                status = list(status.values())
                print("Reservation Status:", status[0])
            else:
                print("Book not found.")
        elif input_text.startswith("LU"):
            self.cursor.execute("""SELECT Books.Status 
                            FROM Books 
                            JOIN Reservations ON Books.BookID = Reservations.BookID
                            JOIN Users ON Reservations.UserID = Users.UserID
                            WHERE Users.UserID = %s""", (input_text,))
            status = self.cursor.fetchone()
            
            if status:
                status = list(status.values())
                print("Reservation Status:", status[0])
            else:
                print("User not found.")
        elif input_text.startswith("LR"):
            self.cursor.execute("""SELECT Books.Status 
                            FROM Books 
                            JOIN Reservations ON Books.BookID = Reservations.BookID
                            WHERE Reservations.ReservationID = %s""", (input_text,))
            status = self.cursor.fetchone()
            
            if status:
                status = list(status.values())
                print("Reservation Status:", status[0])
            else:
                print("Reservation not found.")
        else:
            self.cursor.execute("""SELECT Books.Status 
                            FROM Books 
                            WHERE Books.Title = %s""", (input_text,))
            status = self.cursor.fetchone()
            
            if status:
                status = list(status.values())
                print("Reservation Status:", status[0])
            else:
                print("Book not found.")

        # Find all the books in the database.
        self.cursor.execute("""SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status,
        Users.Name, Users.Email, Reservations.ReservationDate
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Users.UserID = Reservations.UserID""")
        all_books = self.cursor.fetchall()
        if all_books:
            print("All Books:")
            for book in all_books:
                book = list(book.values())
                print("BookID:", book[0])
                print("Title:", book[1])
                print("Author:", book[2])
                print("ISBN:", book[3])
                print("Status:", book[4])
                if book[5]:
                    print("Reserved by:")
                    print("Name:", book[5])
                    print("Email:", book[6])
                    print("Reservation Date:", book[7])
                print()
        else:
            print("No books found in the database.")

        book_id = input("BookID: ")
        self.cursor.execute("""SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status 
                        FROM Books 
                        WHERE Books.BookID = %s""", (book_id,))
        book_details = self.cursor.fetchone()

        if book_details:
            book_details = list(book_details.values())
            print("Book Details:")
            print("BookID:", book_details[0])
            print("Title:", book_details[1])
            print("Author:", book_details[2])
            print("ISBN:", book_details[3])
            print("Status:", book_details[4])
            
            new_status = input("Enter new status: ")
            
            self.cursor.execute("""UPDATE Books 
                            SET Status = %s 
                            WHERE BookID = %s""", (new_status, book_id))
            self.conn.commit()
            print("Book details updated successfully.")
        else:
            print("Book not found.")

        # Delete a book based on its BookID
        book_id = input("The BookID To Delete: ")
        self.cursor.execute("""SELECT Books.BookID 
                        FROM Books 
                        WHERE Books.BookID = %s""", (book_id,))
        book = self.cursor.fetchone()

        if book:
            self.cursor.execute("""DELETE FROM Reservations 
                            WHERE BookID = %s""", (book_id,))
            self.cursor.execute("""DELETE FROM Books 
                            WHERE BookID = %s""", (book_id,))
            self.conn.commit()
            print("Book deleted successfully.")
        else:
            print("Book not found.")

        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    exercise = Exercise4()
    exercise.deal()
