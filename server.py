from flask import Flask, render_template, request, jsonify
import secrets
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def connection_submission():
    if request.method == 'POST':
        print(request.form.get("movie_one"))
        print(request.form.get("movie_two"))

        print(request.form.get("narrative_check") == "on")
        print(request.form.get("theme_check") == "on")
        print(request.form.get("archetype_check") == "on")
        print(request.form.get("other_check") == "on")

        print(request.form.get("connection_explanation", default=""))
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run()