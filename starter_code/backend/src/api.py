import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def retrieve_dinks():
    '''
    Public endpoint: GET to retrieve all drtinks 
    '''
    # query drinks from db 
    selection = Drink.query.all()
    
    if len(selection) == 0:
        abort(404)
        
    else:
        # drinks list in .short() representation
        drinks = [drink.short() for drink in selection]
        
        return jsonify({
            'success': True,
            'drinks': drinks
            })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def drinks_detail(payload):
    '''
    GET Endpoint to retrieve all drtinks-detail to authorized request
    '''
    # query drinks from db 
    selection = Drink.query.all()
    
    if len(selection) == 0:
        abort(404)
        
    else:
        # drinks list in .long() representation
        drinks = [drink.long() for drink in selection]
        
        return jsonify({
            'success': True,
            'drinks': drinks
            })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    '''
    POST endpoint to add a new drink. 
    '''
    # json.dumps() provides a string field for recipe
    body = request.get_json()
    req_title = body.get('title')        
    req_recipe = json.dumps(body.get('recipe'))
    try:
        # create drink with values for each field from the request body
        drink = Drink(
            title=req_title,
            recipe=req_recipe
            )
        
        drink.insert()
        
        # drink.long() returns the new drink array
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })

    except:
        abort(422)
        

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    '''
    PATCH endpoint to update a existing drink. 
    '''
    body = request.get_json()
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    
    if drink is None:
        abort(404)
        
    try:
        # json.dumps() provides a string field for recipe update
        drink = Drink(
            title=body.get('title') ,
            recipe=json.dumps(body.get('recipe'))
            )
        
        drink.update()
        
        # drink.long() returns the new drink array
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })

    except:
        abort(422)
    
'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    '''
    Endpoint for: DELETE a drink
    '''
    # select drink by Drink.id to be passed into the delete() function
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    
    if drink is None:
        abort(404)
        
    if drink:
        drink.delete()

        return jsonify(
            {
                'success': True,
                'delete': id
            }
        )

    else:
        abort(400)



# Error Handling #
'''
Error hnadlers decorators:
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422

@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
            }), 404
    )

'''AuthError with error values imported from auth.auth
'''
@app.errorhandler(AuthError)
def authError(error):
    return (
        jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code
    )

@app.errorhandler(400)
def bad_request(error):
    return (
        jsonify({
                'success': False,
                'error': 400,
                'message': 'bad request'
                }), 400
    )
    
@app.errorhandler(500)
def server_error(error):
    return (
        jsonify({
                'success': False,
                'error': 500,
                'message': 'Internal Server error'
                }), 500
    )