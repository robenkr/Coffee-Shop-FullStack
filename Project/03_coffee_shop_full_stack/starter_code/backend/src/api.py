import os
from flask import Flask, request, jsonify, make_response
from sqlalchemy import exc
import json
from flask_cors import CORS, cross_origin

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

# create and configure the app
app = Flask(__name__)
setup_db(app)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')

    return response


# TODO uncomment the following line to initialize the database
'''
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this functon will add one
'''
db_drop_and_create_all()

# ROUTES

# TODO implement endpoint
'''
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
@cross_origin()
def get_drinks():
    query = Drink.query.order_by(Drink.id).all()

    drinks = [drink.short() for drink in query]

    if len(drinks) == 0:
        return not_found(404)

    return make_response(jsonify({
        "success": True,
        "drinks": drinks
    }))


# TODO implement endpoint
'''
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@cross_origin()
@requires_auth('get:drinks-detail')
def get_drinks_detail(self):
    query = Drink.query.order_by(Drink.id).all()

    drinks = [drink.long() for drink in query]

    if len(drinks) == 0:
        return not_found(404)

    return make_response(jsonify({
        "success": True,
        "drinks": drinks
    }))


# TODO implement endpoint
'''
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@cross_origin()
@requires_auth('post:drinks')
def create_drinks(self):
    body = request.get_json()

    try:
        drink = Drink(
            title=body.get('title', None),
            recipe=json.dumps(body.get('recipe', None))
        )
        drink.insert()

        return make_response(jsonify({
            "success": True,
            "drinks": drink.long()
        }))
    except Exception as e:
        print('ERROR(post:drinks)=>', e)
        return unprocessable(422)


# TODO implement endpoint
'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@cross_origin()
@requires_auth('patch:drinks')
def update_drink(self, drink_id):
    body = request.get_json()

    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if drink is None:
            return not_found(404)

        # Populate Data
        if body.get('title'):
            drink.title = body.get('title')

        if body.get('recipe'):
            drink.recipe = json.dumps(body.get('recipe'))

        drink.update()

        return make_response(jsonify({
            "success": True,
            "drinks": [drink.long()]
        }))
    except Exception as e:
        print('ERROR(patch:drinks)=>', e)
        return unprocessable(422)


# TODO implement endpoint
'''
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@cross_origin()
@requires_auth('delete:drinks')
def delete_drink(self, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if drink is None:
        return not_found(404)

    drink.delete()

    return make_response(jsonify({
        'success': True,
        'deleted': drink_id
    }))


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error, message='unprocessable'):
    return make_response(jsonify({
        "success": False,
        "error": error,
        "message": message
    }), 422)


# TODO implement error handlers using the @app.errorhandler(error) decorator
'''
        each error handler should return (with appropriate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

# TODO implement error handler for 404
'''
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error, message='resource not found'):
    return make_response(jsonify({
        "success": False,
        "error": error,
        "message": message
    }), 404)


# TODO implement error handler for AuthError
'''
    error handler should conform to general task above
'''


@app.errorhandler(401)
def unauthorized(error, message='Unauthorized'):
    return make_response(jsonify({
        "success": False,
        "error": error,
        "message": message
    }), 401)


@app.errorhandler(403)
def forbidden(error, message='Forbidden'):
    return make_response(jsonify({
        "success": False,
        "error": error,
        "message": message
    }), 403)
