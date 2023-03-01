from flask import Flask, render_template, request  # NOT the same as requests
from apis import movie_db_api 

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/get_movie')
def movie_info():
    movie_title = request.args.get('movie_name')
    overview_data = movie_db_api.get_overview(movie_title)
    image_list = movie_db_api.get_image(overview_data['id'])
    genre_list, business_data, production_companies_list = movie_db_api.more_info(overview_data['id'])
    return render_template('movie.html', overview_data=overview_data, image_list=image_list, genre_list=genre_list, business_data=business_data, production_companies_list=production_companies_list)
     


if __name__ == '__main__':
    app.run()