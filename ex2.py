import sqlite3

# Open file and read content as a list
with open('stephen_king_adaptations.txt', 'r') as f:
    read_lines = f.readlines()

# Create connect to database
newConnection = sqlite3.connect('ex2.db')

# Create table 'stephen_king_adaptations_table' if not exits
try:
    conn = newConnection.cursor()
    sql_create = '''CREATE TABLE STEPHEN_KING_ADAPTATIONS_TABLE
    (movieID TEXT PRIMARY KEY NOT NULL,
    movieNAME TEXT NOT NULL,
    movieYEAR INT NOT NULL,
    imdbRATING FLOAT NOT NULL
    );
'''
    conn.execute(sql_create)
except sqlite3.Error as e:
    print(e)

# Read content from file 'stephen_king_adaptations.txt' and insert data into table
for line in read_lines:
    Mid, name, year, rating = line.strip().split(',')
    # print(Mid, name, year, rating)
    sql_insert = '''
        INSERT INTO STEPHEN_KING_ADAPTATIONS_TABLE VALUES ('{}','{}',{},{})
    '''.format(Mid, name, year, rating)
    # print(sql_insert)
    try:
        conn.execute(sql_insert)
    except Exception as e:
        print(e)
    newConnection.commit()

# Loop for user to search movie via different options
opt = 0
while opt != 4:
    print('You can search movie based on following parameters')
    opt = input('1.Movie name\n2.Movie Year\n3.Movie Rating\n4.Stop\n>>')

    # If user choose '1', he can search movie by name
    if opt == '1':
        name = input('Please input the movie name which you want to search >>')
        sql_search_name = '''
            SELECT * FROM STEPHEN_KING_ADAPTATIONS_TABLE WHERE movieNAME = '{}'
        '''.format(name)
        result1 = conn.execute(sql_search_name).fetchall()
        if result1:
            print('The movie\'s details:')
            print('Name: {}, Year: {}, imdbRating: {}'.format(result1[0][1], result1[0][2], result1[0][3]))
        else:
            print('No such movie exists in our database')

    # If user choose '2', he can search movie by year
    elif opt == '2':
        year = input('Please input the year to search movies released in that year >>')
        sql_search_year = '''
            SELECT * FROM STEPHEN_KING_ADAPTATIONS_TABLE WHERE movieYEAR = '{}'
        '''.format(year)
        result2 = conn.execute(sql_search_year).fetchall()
        if result2:
            print('The movies\'s details in that year are as follow >>')
            for movie in result2:
                print('Name: {}, Year: {}, imdbRating: {}'.format(movie[1], movie[2], movie[3]))
        else:
            print('No movie is released in that year')

    # If user choose '3', he can search movie by rating
    elif opt == '3':
        rating = input('Please input the rating to search movies >>')
        sql_search_rating = '''
            SELECT * FROM STEPHEN_KING_ADAPTATIONS_TABLE WHERE imdbRATING >= '{}'
        '''.format(rating)
        result3 = conn.execute(sql_search_rating).fetchall()
        if result3:
            print('The movies are as follow >>')
            for movie in result3:
                print('Name: {}, Year: {}, imdbRating: {}'.format(movie[1], movie[2], movie[3]))
        else:
            print('No movies at or above that rating were found in the database')

    # quit loop when input '4'
    elif opt == '4':
        print('Bye!')
        break
    else:
        print('Please input a correct option')
    x = input('Click enter to continue >>')







