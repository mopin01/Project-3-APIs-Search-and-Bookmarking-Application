from flask import Flask, render_template, request  # NOT the same as requests
from apis import movie_db_api 

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/get_movie')
def movie_info():
    movie_title = request.args.get('movie_name')
    overview, release_date, id, original_title,title = movie_db_api.get_overview(movie_title)
    image_list = movie_db_api.get_image(id)
    for image in image_list:
        print(image)
    return render_template('movie.html', overview=overview, release_date=release_date, id=id, original_title=original_title, title=title, image_list=image_list)
    


if __name__ == '__main__':
    app.run()