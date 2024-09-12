from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL configurations
db_config = {
    'user': 'johnny',
    'password': 'password',
    'host': 'localhost',
    'database': 'fakeHudlDB',
    'raise_on_warnings': True
}

# Function to insert data into the database
def insert_game_data(title, date, gameCode):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Games (Title, Date, GameCode) VALUES (%s, %s, %s)", (title, date, gameCode))
        conn.commit()
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()

# Route for the form page
@app.route('/games')
def games():
    return render_template('game.html')

# Route for the form page
@app.route('/players')
def players():
    return render_template('players.html')

# Route for the form page
@app.route('/notes')
def notes():
    return render_template('notes.html')

# Route for the form page
@app.route('/test')
def notes():
    return render_template('FakeHudl.html')





# Route to handle form submission
@app.route('/submitGame', methods=['POST'])
def submitGame():
    if request.method == 'POST':
        title = request.form['title']
        email = request.form['date']
        gameCode = request.form['gameCode']
        insert_player_data(title, date, gameCode)
        return 'Data inserted successfully'



# Function to insert data into the database
def insert_player_data(playerNumber, playerName):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Players (PlayerNumber, PlayerName) VALUES (%s, %s)", (playerNumber, playerName))
        conn.commit()
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()



# Route to handle form submission
@app.route('/submitPlayer', methods=['POST'])
def submitPlayer():
    if request.method == 'POST':
        playerNumber = request.form['playerNumber']
        playerName = request.form['playerName']
        insert_player_data(playerNumber, playerName)
        return 'Data inserted successfully'


# Function to insert data into the database
def insert_note_data(playeID, note, time, gameID):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Notes (playeID, note, time, gameID) VALUES (%s, %s, %s, %s)", (playeID, note, time, gameID))
        conn.commit()
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()



# Route to handle form submission
@app.route('/submitNote', methods=['POST'])
def submitNote():
    if request.method == 'POST':
        data = request.json
        playerID = data.get('playerID')
        note = data.get('note')
        time = data.get('int')
        gameID = data.get('gameID')
        insert_note_data(playeID, note, time, gameID)
        return 'Data inserted successfully'


if __name__ == '__main__':
    app.run()

