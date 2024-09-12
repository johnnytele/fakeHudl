# flaskapp.py
# This is a "hello world" app sample for flask app. You may have a different file.
from flask import Flask, render_template, request, make_response, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'johnny',
    'password': 'password',
    'host': 'localhost',
    'database': 'fakeHudlDB',
    'raise_on_warnings': True
}

@app.route('/') 
def hello_world():
    games = get_game_with_notes_data()
    players = get_player_name_playerID()
    return render_template('FakeHudl.html', games=games, players=players)

@app.route('/addNote') 
def addNotes():
   games = get_game_data()
   players = get_player_name_number()
   return render_template('addNotes.html', games=games, players=players)


# Route for the form page
@app.route('/test')
def notes():
    games = get_game_with_notes_data()
    players = get_player_name_playerID()
    return render_template('FakeHudl.html', games=games, players=players)

# Route for the form page
@app.route('/addGame')
def addGame():
    return render_template('addGame.html')

@app.route('/addGameUrl')
def addGameUrl():
    return render_template('addGameUrl.html')

@app.route('/summary')
def summaryPage():
    return render_template('summaryPage.html')
'''
# Route for the form page
@app.route('/addPlayer')
def addPlayer():
    return render_template('addPlayer.html')
'''
# Function to insert data into the database
def insert_player_data(playerNumber, playerName):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Players (PlayerNumber, PlayerName) VALUES (%s, %s)", (playerNumber, playerName))
        conn.commit()
        return "Player data inserted successfully."
    except mysql.connector.Error as err:
        print("Error:", err)
        return f"Error occurred: {err}"
    finally:
        cursor.close()
        conn.close()


# Function to insert data into the database
def insert_game_data(title, date, gameCode):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Games (Title, Date, GameCode) VALUES (%s, %s, %s)", (title, date, gameCode))
        conn.commit()
        return "Game data inserted successfully."
    except mysql.connector.Error as err:
        print("Error:", err)
        return f"Error occurred: {err}"
    finally:
        cursor.close()
        conn.close()

# Route to handle form submission
@app.route('/addPlayer', methods=['POST', 'GET'])
def submitPlayer():
    if request.method == 'POST':
        playerNumber = request.form['playerNumber']
        playerName = request.form['playerName']
        result = insert_player_data(playerNumber, playerName)
        # Check the result of the insertion operation
        if "successfully" in result.lower():
            return render_template('addPlayer.html')
        else:
            return make_response(result, 500)  # Internal Server Error
    else:
        return render_template('addPlayer.html')
    

@app.route('/insert_game', methods=['POST'])
def insert_game():

    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        gameCode = request.form['gameCode']
        result = insert_game_data(title, date, gameCode)
        # Check the result of the insertion operation
        if "successfully" in result.lower():
            return render_template('addGame.html')
        else:
            return make_response(result, 500)  # Internal Server Error

@app.route('/insert_game_url', methods=['POST'])
def insert_game_url():

    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        url = request.form['url']
        gameCode = url.split('v=')[1].split('&')[0]
        result = insert_game_data(title, date, gameCode)
        # Check the result of the insertion operation
        if "successfully" in result.lower():
            return render_template('addGame.html')
        else:
            return make_response(result, 500)  # Internal Server Error


# Function to fetch game titles and codes from the database
def get_game_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT Title, GameCode FROM Games")
        games = cursor.fetchall()
        return games
    except mysql.connector.Error as err:
        print("Error:", err)
        return []
    finally:
        cursor.close()
        conn.close()

# Function to fetch game titles and codes from the database
def get_game_with_notes_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT Title, GameCode FROM Games WHERE (SELECT COUNT(*) FROM Notes WHERE Notes.GameID = Games.GameID) > 0 ORDER BY Date DESC, Title")
        games = cursor.fetchall()
        return games
    except mysql.connector.Error as err:
        print("Error:", err)
        return []
    finally:
        cursor.close()
        conn.close()

# Route to handle form submission for adding notes
@app.route('/addNotes', methods=['POST'])
def add_notes():
    if request.method == 'POST':
        message = request.form['message']  # Get the submitted note
        setCode = request.form['selected_set']  # Get the selected game code
        
        # Find the index of the first space
        first_space_index = message.index(' ')

        number_substring = message[1:first_space_index]
        message_without_number = message[first_space_index + 1:]

        second_space_index = message_without_number.index(' ')
        timeSubString = message_without_number[:second_space_index]
        message_cleaned = message_without_number[second_space_index + 1:]

        try:
            minutes, seconds = map(int, timeSubString.split(':'))
            time = minutes * 60 + seconds
        except ValueError:
            print("Invalid time format")



        # Query the database to get the gameID based on the setCode
        gameID   = get_game_id(setCode)
        playerID = get_player_id(number_substring)

        if gameID is not None:
            # Insert the note into the database along with the gameID
            result = insert_game_note(gameID, message_cleaned, playerID, time)
            if "successfully" in result.lower():
                return "Note added successfully."
            else:
                return make_response(result, 500)  # Internal Server Error
        else:
            return make_response("GameID not found. setCode:" + setCode, 404)  # Not Found
    else:
        return "Invalid request method."
    
# Function to get the playerID based on the playerNumber
def get_player_id(playerNumber):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT PlayerID FROM Players WHERE PlayerNumber = %s", (playerNumber,))
        player_id = cursor.fetchone()
        return player_id[0] if player_id else None
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
    finally:
        cursor.close()
        conn.close()

# Function to get the gameID based on the setCode
def get_game_id(setCode):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT GameID FROM Games WHERE GameCode = %s", (setCode,))
        game_id = cursor.fetchone()
        return game_id[0] if game_id else None
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
    finally:
        cursor.close()
        conn.close()

# Function to insert the note into the database
def insert_game_note(gameID, message, playerID, time):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Notes (GameID, Note, PlayerID, Time) VALUES (%s, %s, %s, %s)", (gameID, message, playerID, time))
        conn.commit()
        return "Note added successfully."
    except mysql.connector.Error as err:
        print("Error:", err)
        return f"Error occurred: {err}"
    finally:
        cursor.close()
        conn.close()     

# Function to fetch player numbers and names from the database
def get_player_name_number():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT PlayerNumber, PlayerName FROM Players ORDER BY PlayerNumber ASC")
        players = cursor.fetchall()
        return players
    except mysql.connector.Error as err:
        print("Error:", err)
        return []
    finally:
        cursor.close()
        conn.close()

def get_player_name_playerID():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT PlayerID, PlayerName FROM Players ORDER BY PlayerNumber ASC")
        players = cursor.fetchall()
        return players
    except mysql.connector.Error as err:
        print("Error:", err)
        return []
    finally:
        cursor.close()
        conn.close()
            
@app.route('/getNotes', methods=['GET'])
def getNotes():
    gameCode = request.args.get('setCode')
    playerID = request.args.get('playerID')
    gameID = get_game_id(gameCode)

    if gameID is not None:
        notes = get_notes(gameID, playerID)
        return notes
    return "Failed to get notes for game"

def get_notes(gameID, playerID):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT Note, Time FROM Notes WHERE GameID = %s AND PlayerID = %s ORDER BY Time ASC", (gameID, playerID))
        notes = cursor.fetchall()
        return notes
    except mysql.connector.Error as err:
        print("Error:", err)
        return []
    finally:
        cursor.close()
        conn.close()

@app.route('/getNotesNoPlayer', methods=['GET'])
def getNotesNoPlayer():
    gameCode = request.args.get('setCode')
    gameID = get_game_id(gameCode)

    if gameID is not None:
        notes = get_notes_no_player(gameID)
        return notes
    return "Failed to get notes for game"
    
def get_notes_no_player(gameID):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT Note, Time, NoteID, PlayerName FROM Notes JOIN Players ON Notes.PlayerID = Players.PlayerID WHERE GameID = %s ORDER BY Time ASC", (gameID, ))
        notes = cursor.fetchall()
        return notes
    except mysql.connector.Error as err:
        print("Error:", err)
        return []
    finally:
        cursor.close()
        conn.close()

@app.route('/deleteNote', methods=['POST'])
def deleteNote():
    noteID = request.form['noteID']
    result = delete_note_by_id(noteID)
    return result

def delete_note_by_id(noteID):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Notes WHERE NoteID = %s", (noteID,))
        conn.commit()
        return "Note deleted successfully."
    except mysql.connector.Error as err:
        print("Error:", err)
        return f"Error occurred: {err}"
    finally:
        cursor.close()
        conn.close()

@app.route('/gamesWithNotesByPlayer', methods=['GET'])
def gamesWithNotesByPlayer():
    playerID = request.args.get('playerID')
    games = get_games_with_notes_by_player(playerID)
    return games

def get_games_with_notes_by_player(playerID):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT Title, GameCode, COUNT(NoteID) FROM Games JOIN Notes ON Games.GameID = Notes.GameID WHERE Notes.PlayerID = %s GROUP BY Title, GameCode ORDER BY MAX(Date) DESC, Title", (playerID,))
        games = cursor.fetchall()
        return games
    except mysql.connector.Error as err:
        print("Error:", err)
        return []
    finally:
        cursor.close()
        conn.close()

@app.route('/getNotesSummary', methods=['GET'])
def getNotesSummaryRoute():
    games = getNotesSummary()
    return games


def getNotesSummary():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Games.Title, Date, Players.PlayerName, COUNT(Notes.NoteID), Games.GameID
            FROM Players 
            JOIN Notes ON Players.PlayerID = Notes.PlayerID 
            JOIN Games ON Notes.GameID = Games.GameID 
            GROUP BY Players.PlayerName, Games.Title, Games.Date, Games.GameID
            ORDER BY Games.Date DESC, Games.Title, Players.PlayerName
        """)
        games = cursor.fetchall()
        return games
    except mysql.connector.Error as err:
        print("Error:", err)
        return []
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
   app.run() 