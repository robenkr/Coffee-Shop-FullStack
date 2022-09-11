# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:drinks`
   - `get:drinks-detail`
   - `post:drinks`
   - `patch:drinks`
   - `delete:drinks`
6. Create new roles for:
   - Barista
     - can `get:drinks-detail`
     - can `get:drinks`
   - Manager
     - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 2 users - assign the Barista role to one and Manager role to the other.
   - Sign into each account and make note of the JWT.
   - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
   - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   - Run the collection and correct any errors.
   - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at
  the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application require authentication to retrieve some data.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 404,
    "message": "Not found"
}
```

The API will return two error types when requests fail:

- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 422: Unprocessable

### Endpoints

#### POST /drinks

- General:
  - Creates a new drink using the submitted title and recipe. Returns the created
    drink, and success.
- `curl http://127.0.0.1:5000/drinks -X POST -H "Authorization: Bearer {token}" -H "Content-Type: application/json" -d '{"title": "chilli", "recipe":[{"name": "chilli", "color": "red", "parts": 2}]'`

```
{
    "drinks": {
        "id": 2,
        "recipe": "[{"name": "chilli", "color": "red", "parts": 2}]",
        "title": "chilli"
    },
    "success": true
}
```
#### PATCH /drinks/{drink_id}

- General:
  - Update the drink of the given ID if it exists. Returns the updated drink and success value object.
- `curl http://127.0.0.1:5000/drinks/1 -X PATCH -H "Authorization: Bearer {token}" -H "Content-Type: application/json" -d '{"title": "water", "recipe":[{"name": "water", "color": "black", "parts": 2}]'`

```
{
    "drinks": {
        "id": 1,
        "recipe": [
            {
                "color": "black",
                "name": "water",
                "parts": 2
            }
        ],
        "title": "water"
    },
    "success": true
}
```
#### DELETE /drinks/{drink_id}

- General:
  - Deletes the drink of the given ID if it exists. Returns the id of the deleted drink and success value.
- `curl -X DELETE -H "Authorization: Bearer {token}" http://127.0.0.1:5000/drinks/1`

```
{
    "deleted": 1,
    "success": true
}
```
#### GET /drinks

- General:
  - Returns a short list of drinks objects and success value.
- Sample: `curl http://127.0.0.1:5000/drinks`

``` 
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 1
                }
            ],
            "title": "water"
        },
        {
            "id": 2,
            "recipe": [
                {
                    "color": "brown",
                    "parts": 2
                },
                {
                    "color": "blue",
                    "parts": 2
                },
                {
                    "color": "white",
                    "parts": 1
                },
                {
                    "color": "green",
                    "parts": 1
                }
            ],
            "title": "ginger light"
        }
    ],
    "success": true
}
```

#### GET /drinks-detail

- General:
  - Returns a long(detailed) list of drinks objects and success value.
- Sample: `curl http://127.0.0.1:5000/drinks-detail`

``` 
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "water"
        },
        {
            "id": 2,
            "recipe": [
                {
                    "color": "brown",
                    "name": "ginger",
                    "parts": 2
                },
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 2
                },
                {
                    "color": "white",
                    "name": "sugar",
                    "parts": 1
                },
                {
                    "color": "green",
                    "name": "lemon",
                    "parts": 1
                }
            ],
            "title": "ginger light"
        }
    ],
    "success": true
}
```