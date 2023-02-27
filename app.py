from flask import Flask, render_template, request  # NOT the same as requests
from apis import movie_db_api 

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/get_movie')
def movie_info():
    movie_title = request.args.get('movie_name')
    print(movie_title)
    overview, release_date, id, original_title = movie_db_api.get_overview(movie_title)
    return render_template('movie.html', overview=overview, release_date=release_date, id=id, original_title=original_title)
    


if __name__ == '__main__':
    app.run()