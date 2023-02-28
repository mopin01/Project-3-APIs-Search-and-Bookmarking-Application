# Movie API Search Tool

The user will enter a search query (actor, movie title etc). The app will contact the moviedb API to request search query data (like overview, release date etc) ; youtube API to request trailers data; and wikipedia API to request more background data (like casts etc). The app will present this data to the user in this way: web application

## Built With

```
,___________,         .----------,   Request     .------------,       .----------.
|___________|       ,'_________,'|   -> | ->   ,'___________,'|      ( ~--------~ )
| HTML5     |      | Flask     | |      |      | Python     | |      | SQLite     |
| CSS3      |      |           | |      |      | Requests   | |      |            |
|           |      |           | |      |      | dotenv     | |      |            |
|           | <--- |           | |      |      |            | | <--- |            |
|           |      |           | |      |      |            | |      |            |
|           |      |           | |      |      |            | |      |            |
|           |      |           | ;   <- | <-   |            | ;      | ~--------~ |
|___________|      |___________|'   Response   |____________|'       `.__________.'
   Client           Client Logic             Server & Middleware        Database
           *Front End*                                       *Back End*
```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. You can either fork this repoistory and then clone it from your computer or you can download the zip file.

### Prerequisites

- [Python](https://www.python.org/downloads/)
- [Sqlite](https://www.sqlite.org/index.html)
- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- [Python-dotenv](https://pypi.org/project/python-dotenv/)
- [Requests](https://pypi.org/project/requests/)

### Installing

Once you clone the repo, you will want to install all the modules so that the repo should function properly.

1. Create a [OMDB API key](http://www.omdbapi.com/).
2. Create a [Youtube API key](https://developers.google.com/youtube/v3)
3. Create an `.env` with your API keys.

- To utilize API keys, you will need to create a .env file in your main directory. You will not be able to upload it to this repo as most .gitignore will ignore the file. This is for security reasons as you do not want to post your API Keys to these services out in the open. When you are done creating the .env file, insert your respective keys into the text below and then save the .env file.

```
export MOVIE_API_KEY='INSERT MOVIE_API_KEY KEY HERE'
export YOUTUBE_API_KEY='INSERT YOUTUBE_API_KEY AUTH_TOKEN KEY HERE'
```

## Usage

To run the application, enter the following in the terminal:

```
flask run
```

App will be running on http://127.0.0.1:5000

## Authors

- Abdirahman Ali
- Carter Klimek
- James Nguyen
- Tenzin Minleg
