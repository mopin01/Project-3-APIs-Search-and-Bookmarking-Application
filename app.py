from flask import Flask, render_template, make_response, request  # NOT the same as requests
from apis import movie_db_api 
from apis import moviequotes_api
from apis import imbd_api
from apis import youtube_trailer_api
from databases.bookmarks import Bookmarks
from databases.cache import Cache
import json

app = Flask(__name__)
bookmarks = Bookmarks()
cache = Cache()

@app.route('/')
def homepage():
    movie_quote = moviequotes_api.get_quote()
    return render_template('index.html', movie_quote=movie_quote)

@app.route('/search_movies')
def search():
    movie_title = request.args.get('movie_name')
    search_movies = imbd_api.search_movies(movie_title)
    if not movie_title:
        return render_template('error.html', message='Please enter a movie title')
    return render_template('search.html', movie_title=movie_title, search_movies=search_movies)

@app.route('/get_movie')
def movie_info():
    movie_title = request.args.get('movie_name')
    if not cache.movie_exists(movie_title):
        overview_data = movie_db_api.get_overview(movie_title)
        imbd_data = imbd_api.get_imbd_data(movie_title)
        youtube_trailer = youtube_trailer_api.get_movie_trailer(movie_title)
        wikipedia_summary = imbd_api.get_wikipedia_data(imbd_data['id'])
        image_list = movie_db_api.get_image(overview_data['id'])
        genre_list, business_data, production_companies_list = movie_db_api.more_info(overview_data['id'])

        data = {
            'overview_data' : overview_data,
            'business_data' : business_data,
            'wikipedia_summary' : wikipedia_summary,
            'production_companies_list' : production_companies_list,
            'image_list' : image_list,
            'genre_list' : genre_list,
            'youtube_trailer' : youtube_trailer
        }

        data = format_data(data)
        cache.add_movie(data)
    else:
        data = cache.get_movie_by_title(title)

    return render_template('movie.html', data=extract_data(data), is_bookmarked=bookmarks.movie_exists(title))

def format_data(data):
    new_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                new_data[sub_key] = sub_value
        else:
            new_data[key] = json.dumps(value)
    return new_data

def extract_data(data):
    for key, value in data.items():
        try:
            data[key] = json.loads(value)
        except:
            pass
    return data

@app.route('/post_quote/')
def post_quote():
    movie_quote = moviequotes_api.get_quote()
    return render_template('quote.html', movie_quote=movie_quote )

@app.route('/add_bookmark/')
def add_bookmark():
    title = request.args.get('title')
    data = cache.get_movie_by_title(title)
    bookmarks.add_movie(data)
    return make_response("", 204)

@app.route('/delete_bookmark/')
def delete_bookmark():
    title = request.args.get('title')
    bookmarks.delete_movie(title)
    return make_response("", 204)

@app.route('/show_bookmarks/')
def show_bookmarks():
    movie_titles = bookmarks.get_all_titles()
    return render_template('bookmarks.html', movie_titles=movie_titles)

@app.route('/view_bookmark')
def view_bookmark():
    title = request.args.get('title')
    data = bookmarks.get_movie_by_title(title)
    return render_template('movie.html', data=extract_data(data), is_bookmarked=True)

@app.errorhandler(Exception)
def handle_error(e):
    return render_template('error.html', error=e)

if __name__ == '__main__':
    app.run()