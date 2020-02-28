# Auto Repair App ✍
### API Core Services

Provides the core api functionality for auto repair


## API

This App exposes endpoints that allows ```clients/Users``` to interact with basic services.


#### Available Resource Endpoints

|Method | Endpoint | Usage |
| ---- | ---- | --------------- |
|POST| `url/here` | description here.|
|GET| `url/here` | description here.|


# Getting Started 🕵


## Prerequisites
- The application is built using python: Flask framework.
>[Flask](http://flask.pocoo.org/) is a micro-framework for the Python programming language.

- To Install python checkout:

    - *https://www.python.org/*


- Docker is central in developing and deploying this application
>[Docker](https://www.docker.com/get-started)

- To install docker checkout:

    - *https://www.docker.com/products/docker-desktop*



## Clone the project
- To run on local machine git clone this project
```bash
 $ git clone https://georgreen@bitbucket.org/georgreen/core-service-api.git
```


## Installing

- For this section I will assume you have python3 and it's configured on your machine.
- Navigate to the folder you cloned and run:

```bash
$ cd core-services-api
```


## Install Requirements

```bash
$ pipenv install
```


## Build App

```bash
$ docker-compose -f docker-compose-dev.yml build
```


## Run App 🏃

```bash
$ docker-compose -f docker-compose-dev.yml up
```

- The app should be accessible via : http://127.0.0.1:5000/


## Running the tests

```bash
$ docker-compose -f docker-compose-dev.yml run core-api python manage.py test
```

- Coding style tests

[PEP8](https://pypi.org/project/pycodestyle/) (pycodestyle) standards are followed in project. </br>
PEP8 has deprecated; instead use pycodestyle for the same effect

```bash
$ docker-compose -f docker-compose-dev.yml exec core-api pycodestyle .
```


## Database Seeding

- Seed the database.

```bash
$ docker-compose -f docker-compose-dev.yml exec core-api python manage.py seed
```


## Deployment 🚀

- Aws


## Built With  🏗 🔨⚒

* [Flask](http://flask.pocoo.org/) - The web framework used


## Contributing 👍

- Closed


## Versioning ⚙

- MVP


## Authors 📚

- Devs


## License 🤝

- This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
