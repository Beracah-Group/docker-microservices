# Auto Repair ✍
### API for Core Services.

Provides the core api functionality for auto repair


## API

This App exposes endpoints that allows ```clients/Users``` to interact with basic services.

#### Available Resource Endpoints

|Method | Endpoint | Usage |
| ---- | ---- | --------------- |
|POST| `url/here` | description here.|
|GET| `url/here` | description here.|


## Getting Started 🕵
- To run on local machine git clone this project :

```
 $ git clone https://georgreen@bitbucket.org/georgreen/core-service-api.git
 ```

 Copy and paste the above command in your terminal, the project will be downloaded to your local machine.

- To consume API in client of choice navigate to:

 ```
 http://
 ```

### Prerequisites
The application is built using python: Flask framework.
>[Flask](http://flask.pocoo.org/) is a micro-framework for the Python programming language.


To Install python checkout:

```
https://www.python.org/
```


### Installing

For this section I will assume you have python3 and it's configured on your machine. </br>
Navigate to the folder you cloned and run: </br>

- Install Requirements

```
$ cd src
$ pipenv install
```

- Configure Environment

```
export SECRET="Thequickbrownfoxjumpedoverthelazydog"
export APP_SETTINGS=Development
export DEV_DATABASE=database_url_for_development_environment
export TEST_DATABASE=database_url_for_testing_environment
```

> Note replace the value for DATABASE_URL & TEST_DATABASE with a real database path and SECRET with a strong string value

- Run App 🏃

```
$ cd src
$ python manage.py runserver
```

The app should be accessible via : http://127.0.0.1:5000/


## Running the tests

```
$ cd src
$ python manage.py test
```

- Coding style tests

[PEP8](https://pypi.org/project/pycodestyle/) (pycodestyle) standards are followed in project. </br>
PEP8 has deprecated; instead use pycodestyle for the same effect

```
$ cd src
$ pycodestyle .

```

## Database Seeding

Seed the database.

```
$ python manage.py db seed
```

## Running the sandbox


## Deployment 🚀

- [Check this out to deploy to heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)

## Built With  🏗 🔨⚒

* [Flask](http://flask.pocoo.org/) - The web framework used
* [Flaskrestplus](https://flask-restplus.readthedocs.io/en/stable/) - Extension for Flask that adds support for quickly building REST APIs.

## Contributing 👍

closed

## Versioning ⚙


## Authors 📚


## License 🤝

- This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

