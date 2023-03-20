from flask import Flask, render_template, request  # NOT the same as requests
from apis import movie_db_api 
from apis import moviequotes_api
from apis import imbd_api
from databases.bookmarks import Bookmarks
from databases.cache import Cache
import json

app = Flask(__name__)
bookmarks = Bookmarks()
cache = Cache()

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/get_movie')
def movie_info():
    movie_title = request.args.get('movie_name')
    overview_data = movie_db_api.get_overview(movie_title)
    imbd_data = imbd_api.get_imbd_data(movie_title)
    wikiedia_summary = imbd_api.get_wikipedia_data(imbd_data['id'])
    image_list = movie_db_api.get_image(overview_data['id'])
    genre_list, business_data, production_companies_list = movie_db_api.more_info(overview_data['id'])


    return render_template('movie.html', overview_data=overview_data, wikiedia_summary=wikiedia_summary, image_list=image_list, genre_list=genre_list, business_data=business_data, production_companies_list=production_companies_list)

    # TEMPORARY- Condenses data into single list for database
    data = {}
    data.update(**overview_data)
    data['image_list'] = json.dumps(image_list)
    data['genre_list'] = json.dumps(genre_list)
    data.update(**business_data)
    data['production_companies_list'] = json.dumps(production_companies_list)
    cache.add_movie(data)

    return render_template('movie.html', overview_data=overview_data, wikiedia_summary=wikiedia_summary, image_list=image_list, genre_list=genre_list, business_data=business_data, production_companies_list=production_companies_list)

@app.route('/post_quote/')
def post_quote():
    movie_quote = moviequotes_api.get_quote()
    return render_template('quote.html', movie_quote=movie_quote )

@app.route('/add_bookmark/')
def add_bookmark():
    title = request.args.get('title')
    data = cache.get_movie(title)
    bookmarks.add_movie(data)
    return render_template('index.html')

@app.route('/show_bookmarks/')
def show_bookmarks():
    movie_titles = bookmarks.get_all_titles()
    return render_template('bookmarks.html', movie_titles=movie_titles)

@app.route('/view_bookmark')
def view_bookmark():
    title = request.args.get('title')
    data = bookmarks.get_movie_by_title(title)

    # TEMPORARY- Extracts and formats data to be passed to movie.html
    overview_data = {
        'id' : data['id'],
        'original_title' : data['original_title'],
        'title' : data['title'],
        'release_date' : data['release_date'],
        'overview' : data['overview']
    }
    image_list = json.loads(data['image_list'])
    genre_list = json.loads(data['genre_list'])
    business_data = {
        'budget' : data['budget'],
        'revenue' : data['revenue']
    }
    production_companies_list = json.loads(data['production_companies_list'])

    return render_template('movie.html', overview_data=overview_data, image_list=image_list, genre_list=genre_list, business_data=business_data, production_companies_list=production_companies_list)

if __name__ == '__main__':
    app.run()