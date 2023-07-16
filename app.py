from flask import Blueprint, render_template, Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
import io
import imdb
import pandas as pd

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html")

@views.route('/handle_event/<data>', methods=['GET', 'POST'])
def handle_event(data):

    # Return a JSON response
    if request.method == 'POST':
        print('handled')
        redirect(url_for("views.home2"))
        return redirect(url_for("views.home2"))
    
    print('get')
    print(request.method)
    return render_template("new_screen.html", data=data)

@views.route("/new_screen/<data>")
def home2(data):
    return render_template("new_screen.html", data = data)

ia = imdb.Cinemagoer()
app = Flask(__name__)
CORS(app, resources={r"/upload": {"origins": "*"}, r"/upload": {"methods": ["POST"]}})
app.register_blueprint(views, url_prefix="/views")

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        try:
            file_data = request.get_data()
            decoded_data = file_data.decode('utf-8')
        # Process the file data
            return process_file(decoded_data)
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500
    
def process_file(file_data):
    try:
        # Create a StringIO object to mimic a file-like object
        file_buffer = io.StringIO(file_data)
        # Read the CSV file using pandas
        df = pd.read_csv(file_buffer)
        first_column = df.iloc[:, 0]
        sec_column = df.iloc[:, 1]
        Occurances = {}
        Genres = {}
        MoviesDict = {}
        Cast = {}
        freq = {}
        max = 0
        maxDate = ""
        for value in sec_column:
            print(value)
            if value in freq:
                freq[value] = freq[value] + 1
                if freq[value] > max:
                    max = freq[value]
                    maxDate = value    
            else:
                freq[value] = 1

# Iterate through the values in the first column
        for value in first_column:
    # Do something with each value
            if ":" in value:
                value = value.split(":")[0]
            if value in Occurances:
                Occurances[value] = Occurances[value] + 1
            else:
                Occurances[value] = 1
        OccurancesOrdered = sorted(Occurances.items(), key=lambda x:x[1])
        orderedDict = dict(OccurancesOrdered)
        count = 0
        topShows = []
        topGenres = []
        topActors = []
        topDate = []
        topDate.append(maxDate)

        for x in list(reversed(list(orderedDict)))[0:10]:
                movies = ia.search_movie(x)
                movie = ia.get_movie(movies[0].movieID)

                count = count + 1
                topShows.append(movies[0]['title'])
                for cast in movie['cast']:
                    if cast in Cast:
                        Cast[cast] = Cast[cast] + 1
                    else:
                        Cast[cast] = 1
                for genre in movie['genres']:
                    if genre in Genres:
                        Genres[genre] = Genres[genre] + 1
                    else:
                        Genres[genre] = 1


        GenresOrdered = sorted(Genres.items(), key=lambda x:x[1])
        orderedGenre = dict(GenresOrdered)
        for x in list(reversed(list(orderedGenre)))[0:5]:
            topGenres.append(x)

        CastOrdered = sorted(Cast.items(), key=lambda x:x[1])
        orderedCast = dict(CastOrdered)
        for x in list(reversed(list(orderedCast)))[0:3]:  
            topActors.append(x['name'])

        data = [topActors, topGenres, topShows]
        return data
        # Function to process a batch of keys
    except Exception as e:
        error_message = str(e)
        print(f"An error occurred: {error_message}")


if __name__ == '__main__':
    app.run(debug=True, port=8000)
