from flask import Blueprint, request,jsonify
from marvel_inventory.helpers import token_required
from marvel_inventory.models import db, User, Character, marvel_schema, marvel_schemas

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return { 'some': 'value'}


# Create Marvel Endpoint
@api.route('/characters',methods = ['POST'])
@token_required
def create_character(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    character = Character(name,description,comics_appeared_in,super_power,user = user_token)

    db.session.add(character)
    db.session.commit()

    response = marvel_schema.dump(character)
    return jsonify(response)


 # Retrieve all characters endpoint
@api.route('/characters', methods = ['GET'])
@token_required
def get_characters(current_user_token):
    owner = current_user_token.token
    character = Character.query.filter_by(user = owner).all()
    response = marvel_schemas.dump(character)
    return jsonify(response)

# Retrieve one characters endpoint
@api.route('/characters/<id>', methods =['GET'])
@token_required
def get_character(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        character = Character.query.get(id)
        response = marvel_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({'message': "Valid Token Required"}), 401

# UPDATE characters ENDPOINT
@api.route('/characters/<id>', methods = ['POST','PUT'])
@token_required
def update_character(current_user_token,id):
    character = Character.query.get(id) 
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    date_created = request.json['date_created']
    user_token = current_user_token.token

    db.session.commit()
    response = marvel_schema.dump(character)
    return jsonify(response)

# DELETE character ENDPOINT
@api.route('/characters/<id>', methods = ['DELETE'])
@token_required
def delete_characters(current_user_token, id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()
    response = marvel_schema.dump(character)
    return jsonify(response)