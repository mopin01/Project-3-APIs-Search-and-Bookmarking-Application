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
    try:
        movie_quote = moviequotes_api.get_quote()
        return render_template('index.html', movie_quote=movie_quote)
    except Exception as e:
        return render_template('error.html', message='Error: Unable to retrieve movie quote. ' + str(e))

@app.route('/search_movies')
def search():
    movie_title = request.args.get('movie_name')
    search_movies = imbd_api.search_movies(movie_title)
    if not movie_title:
        return render_template('error.html', message='Please enter a movie title')
    return render_template('search.html', movie_title=movie_title, search_movies=search_movies)

@app.route('/get_movie/<title>')
def movie_info(title):
    try:
        if not cache.movie_exists(title):
            overview_data = movie_db_api.get_overview(title)
            image_list = movie_db_api.get_image(overview_data['id'])
            genre_list, business_data, production_companies_list = movie_db_api.more_info(overview_data['id'])
            imbd_data = imbd_api.get_imbd_data(title)
            wikipedia_summary = imbd_api.get_wikipedia_data(imbd_data['id'])
            youtube_trailer = youtube_trailer_api.get_movie_trailer(title)

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
            data = cache.get_movie_by_title(movie_title)

        return render_template('movie.html', data=extract_data(data), is_bookmarked=bookmarks.movie_exists(movie_title))
    except ValueError as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)
    except Exception as e:
        error_message = "An error occurred while processing your request. Please try again later."
        return render_template('error.html', error_message=error_message)

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

@app.route('/add_bookmark/')
def add_bookmark():
    try:
        title = request.args.get('title')
        data = cache.get_movie_by_title(title)
        bookmarks.add_movie(data)
        return make_response("", 204)
    except Exception as e:
        return render_template('error.html', message="Unable to add bookmark. Please try again later.")


@app.route('/delete_bookmark/')
def delete_bookmark():
    try:
        title = request.args.get('title')
        bookmarks.delete_movie(title)
        return make_response("", 204)
    except Exception as e:
        return make_response(f"Error deleting bookmark: {e}", 500)


@app.route('/show_bookmarks/')
def show_bookmarks():
    try:
        movie_titles = bookmarks.get_all_titles()
        return render_template('bookmarks.html', movie_titles=movie_titles)
    except Exception as e:
        return render_template('error.html', message="Unable to access the database. Please try again later.")


@app.route('/view_bookmark')
def view_bookmark():
    title = request.args.get('title')
    try:
        data = bookmarks.get_movie_by_title(title)
        return render_template('movie.html', data=extract_data(data), is_bookmarked=True)
    except Exception as e:
        return render_template('error.html', message="Unable to access the database. Please try again later.")


@app.errorhandler(Exception)
def handle_error(e):
    return render_template('error.html', error=e)

if __name__ == '__main__':
    app.run()