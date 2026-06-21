from flask import Flask, render_template, request, jsonify, g
import secrets
import requests
import sqlite3
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def init_db():
    db_path = os.path.join(app.instance_path, "jamovies.db")
    connection = sqlite3.connect(db_path)

    connection.execute("CREATE TABLE IF NOT EXISTS connections(connection_id INTEGER PRIMARY KEY AUTOINCREMENT, movie_one_title TEXT NOT NULL, movie_two_title TEXT NOT NULL, movie_one_poster TEXT, movie_two_poster TEXT, narrative_check BOOLEAN, theme_check BOOLEAN, archetype_check BOOLEAN, other_check BOOLEAN, connection_explanation TEXT, date TEXT DEFAULT CURRENT_TIMESTAMP)")
    connection.commit()
    connection.close()


def get_db():
    db = getattr(g, "_database", None)
    db_path = os.path.join(app.instance_path, "jamovies.db")
    if db is None:
        db = g._database = sqlite3.connect(db_path)
        db.row_factory = sqlite3.Row 
    return db

@app.route('/', methods=['GET', 'POST'])
def connection_submission():
    if request.method == 'POST':
        movie_one_title = request.form.get("movie_one_title")
        movie_two_title = request.form.get("movie_two_title")
        movie_one_poster = request.form.get("movie_one_poster")
        movie_two_poster = request.form.get("movie_two_poster")
        narrative_check = request.form.get("narrative_check") == ("on")
        theme_check = request.form.get("theme_check") == ("on")
        archetype_check = request.form.get("archetype_check") == ("on")
        other_check = request.form.get("other_check") == ("on")
        connection_explanation = request.form.get("connection_explanation", default="")

        db = get_db()
        db.execute(
            "INSERT INTO connections "
            "(movie_one_title, movie_two_title, movie_one_poster, movie_two_poster, narrative_check, theme_check, archetype_check, other_check, connection_explanation) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            (movie_one_title, movie_two_title, movie_one_poster, movie_two_poster, narrative_check, theme_check, archetype_check, other_check, connection_explanation)
        )
        db.commit()
    return render_template('home.html')

@app.route('/search')
def movies():
    query = request.args.get('query')
    resp = requests.get(
        'https://api.themoviedb.org/3/search/movie?query=' + query,
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + secrets.API_TOKEN
        }
    )
    return jsonify(resp.json())

@app.route('/connections')
def view_connections():
    db = get_db()
    connections = db.execute(
        "SELECT * FROM connections ORDER BY date DESC"
        ).fetchall()
    return render_template('connections.html', connections=connections)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    init_db()
    app.run()