"""
ENDPOINTS , tmb importamos aqui las clases del models.py
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Planets,Characters,Spaceships,FavoritePlanets,FavoriteCharacters,FavoriteSpaceships
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


"""
USERS BELOW HERE (6 Endpoints)
"""

@app.route('/user', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    all_users_serialize = []

    for user in all_users:
        all_users_serialize.append(user.serialize())

    response_body = {
        "msg": "Hello, this is your GET /user response to see all the users",
        "data": all_users_serialize
    }
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    single_user = User.query.get(user_id)
    if single_user == None:
        return jsonify({'msg': f'User with id: {user_id} doesn\'t exist'} ),404
    return jsonify({'msg':'ok',
                    'data': single_user.serialize()}),200

@app.route('/user', methods=['POST'])
def create_user():
    user_data = request.get_json()

    if not user_data.get('user_name') or not user_data.get('email') or not user_data.get('password'):
        return jsonify({'msg': 'Fields required: (user_name, email, password)'}), 400
    existing_user = User.query.filter_by(email=user_data['email']).first()
    if existing_user:
        if not existing_user.is_active:
            existing_user.is_active = True
            db.session.commit()
            return jsonify({'msg': 'User successfully reactivated', 'data': existing_user.serialize()}), 200
        else:
            return jsonify({'msg': 'This email is already in use by an active user'}), 409

    new_user = User(
        user_name=user_data['user_name'],
        email=user_data['email'],
        password=user_data['password'],
        is_active=True
    )
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Error creating the user', 'error': str(e)}), 500

    return jsonify({'msg': 'User successfully created', 'data': new_user.serialize()}), 201

@app.route('/user/<int:user_id>', methods=['DELETE'])
def deactivate_user(user_id):
    user_to_deactivate = User.query.get(user_id)
    if user_to_deactivate is None:
        return jsonify({'msg': f'User with id: {user_id} doesnt exist'}), 404
    
    if user_to_deactivate.is_active == False:
        return jsonify({'msg': f'User with id: {user_id} is already deactivated'}), 409
    
    user_to_deactivate.is_active = False

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Error erasing user', 'error': str(e)}), 500

    return jsonify({'msg': f'User with id: {user_id} deactivated'}), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):

    user_to_update = User.query.get(user_id)
    if user_to_update is None:
        return jsonify({'msg': f'User with id: {user_id} doesn\'t exist'}), 404
    if user_to_update.is_active == False:
        return jsonify({'msg': f'User with id: {user_id} is deactivated'}), 409

    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400

    if 'email' not in body or'user_name' not in body or'password' not in body:
        return jsonify({'msg': 'Fields "email" and "user_name" are mandatory'}), 400
    
    user_data = request.get_json()
    user_to_update.email = user_data['email']
    user_to_update.password = user_data['password']
    user_to_update.user_name = user_data['user_name']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Error al actualizar el usuario', 'error': str(e)}), 500

    return jsonify({'msg': f'Usuario con id {user_id} actualizado exitosamente', 'data': user_to_update.serialize()}), 200

@app.route('/user/<int:id_user>/favorites', methods=['GET'])
def get_favorites(id_user):

    user = User.query.get(id_user)
    if user is None:
        return jsonify({'msg': f'User with id: {id_user} doesn\'t exist'}), 404
    
    favorite_planets = FavoritePlanets.query.filter_by(user_id=id_user).all()
    favorite_spaceships = FavoriteSpaceships.query.filter_by(user_id=id_user).all()
    favorite_characters = FavoriteCharacters.query.filter_by(user_id=id_user).all()

    favorite_planets_serialize = []
    for fav in favorite_planets:
        favorite_planets_serialize.append(fav.planet_relationship.serialize())
    
    favorite_characters_serialize = []
    for fav in favorite_characters:
        favorite_characters_serialize.append(fav.character_relationship.serialize())
    
    favorite_spaceships_serialize = []
    for fav in favorite_spaceships:
        favorite_spaceships_serialize.append(fav.spaceship_relationship.serialize())

    return jsonify({
        'a_msg': f'All the favorites from user id: {id_user} are those:',
        'data': {
        'favorite_planets': favorite_planets_serialize,
        'favorite_spaceships': favorite_spaceships_serialize,
        'favorite_characters': favorite_characters_serialize,
        }
    }), 200


"""
PLANETS BELOW HERE (7 Endpoints)
"""

@app.route('/planets', methods=['GET'])
def get_all_planets():
    # Retrieve all planets from the database
    all_planets = Planets.query.all()
    # Serialize each planet into a dictionary
    all_planets_serialize = [planet.serialize() for planet in all_planets]
    response_body = {
        "msg": "Hello, this is your GET /planets response to see all the planets",
        "data": all_planets_serialize
    }
    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    # Retrieve a single planet by its ID
    single_planet = Planets.query.get(planet_id)
    if single_planet is None:
        return jsonify({'msg': f'Planet with id: {planet_id} doesn\'t exist'}), 404
    return jsonify({
        'msg': 'Hello, this is your GET /planet response to see one singular planet',
        'data': single_planet.serialize()
    }), 200

@app.route('/planet', methods=['POST'])
def add_planet():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({'msg': 'You must send info in the body'}), 400

    # Check for required fields in the request body
    required_fields = ['name', 'diameter', 'population', 'duration_day', 'terrain']
    if not all(field in body for field in required_fields):
        return jsonify({'msg': 'Fields "name", "diameter", "population", "duration_day", and "terrain" are mandatory'}), 400

    # Check if a planet with the same name already exists
    if Planets.query.filter_by(name=body['name']).first():
        return jsonify({'msg': 'A planet with this name already exists'}), 400

    # Create a new planet entry
    new_planet = Planets(
        name=body['name'],
        diameter=body['diameter'],
        population=body['population'],
        duration_day=body['duration_day'],
        terrain=body['terrain']
    )
    db.session.add(new_planet)
    db.session.commit()

    return jsonify({
        'msg': 'New planet created!',
        'data': new_planet.serialize()
    }), 201

@app.route('/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    body = request.get_json(silent=True)
    # Retrieve the existing planet by its ID
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': f'Planet with id: {planet_id} doesn\'t exist'}), 404

    if not body:
        return jsonify({'msg': 'You must send info in the body'}), 400

    # Check for required fields in the request body
    required_fields = ['name', 'diameter', 'population', 'duration_day', 'terrain']
    if not all(field in body for field in required_fields):
        return jsonify({'msg': 'Fields "name", "diameter", "population", "duration_day", and "terrain" are mandatory'}), 400

    # Update the planet's attributes
    planet.name = body['name']
    planet.diameter = body['diameter']
    planet.population = body['population']
    planet.duration_day = body['duration_day']
    planet.terrain = body['terrain']
    
    db.session.commit()
    return jsonify({
        'msg': f'Planet with id: {planet_id} modified!',
        'data': planet.serialize()
    }), 200

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    # Retrieve the planet by its ID
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': f'Planet with id: {planet_id} doesn\'t exist'}), 404
    
    # Check if there are existing favorite relationships for this planet
    existing_favorites = FavoritePlanets.query.filter_by(planet_id=planet_id).all()
    if existing_favorites:
        return jsonify({'msg': f'Please delete the favorite relationships for planet with id: {planet_id} before deleting the planet'}), 400
    
    # Delete the planet from the database
    db.session.delete(planet)
    db.session.commit()
    
    return jsonify({'msg': f'Planet with id: {planet_id} erased'}), 200

# Post Favorite Planet
@app.route('/favorite/planet/<int:planet_id>/<int:user_id>', methods=['POST'])
def add_favorite_planet(planet_id, user_id):
    # Retrieve the user and planet by their IDs
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)
    
    if user is None:
        return jsonify({'msg': f'User with id: {user_id} doesn\'t exist'}), 404
    if not user.is_active:
        return jsonify({'msg': f'User with id: {user_id} is deactivated'}), 409
    if planet is None:
        return jsonify({'msg': f'Planet with id: {planet_id} doesn\'t exist'}), 404
    
    # Check if the user already has this planet as a favorite
    existing_favorite = FavoritePlanets.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favorite:
        return jsonify({'msg': f'Planet with id: {planet_id} is already a favorite for user with id: {user_id}'}), 409
    
    # Create a new favorite relationship
    new_relationship = FavoritePlanets(
        user_id=user_id,
        planet_id=planet_id
    )
    db.session.add(new_relationship)
    db.session.commit()

    return jsonify({'msg': f'Planet with id: {planet_id} added as favorite for user with id: {user_id}'}), 200

# Delete Favorite Planet
@app.route('/favorite/planet/<int:planet_id>/<int:user_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id, user_id):
    # Retrieve the user and planet by their IDs
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)
    
    if user is None:
        return jsonify({'msg': f'User with id: {user_id} doesn\'t exist'}), 404
    if not user.is_active:
        return jsonify({'msg': f'User with id: {user_id} is deactivated'}), 409
    if planet is None:
        return jsonify({'msg': f'Planet with id: {planet_id} doesn\'t exist'}), 404
    
    # Check if the user has this planet as a favorite
    existing_favorite = FavoritePlanets.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favorite is None:
        return jsonify({'msg': f'Favorite relationship between user id: {user_id} and planet id: {planet_id} doesn\'t exist'}), 404
    
    # Delete the favorite relationship
    db.session.delete(existing_favorite)
    db.session.commit()

    return jsonify({'msg': f'Planet with id: {planet_id} deleted from favorites for user with id: {user_id}'}), 200


"""
SPACESHIPS BELOW HERE (7 Endpoints)
"""

@app.route('/spaceships', methods=['GET'])
def get_all_spaceships():
    all_spaceships = Spaceships.query.all()
    all_spaceships_serialize = []
    for spaceship in all_spaceships:
        all_spaceships_serialize.append(spaceship.serialize())
    response_body = {
        "msg": "Hello, this is your GET /spaceships response to see all the spaceships",
        "data": all_spaceships_serialize
    }
    return jsonify(response_body), 200

@app.route('/spaceship/<int:spaceship_id>', methods=['GET'])
def get_single_spaceship(spaceship_id):
    single_spaceship = Spaceships.query.get(spaceship_id)
    if single_spaceship is None:
        return jsonify({'msg': f'Spaceship with id: {spaceship_id} doesn\'t exist'}), 404
    return jsonify({
        'msg': 'Hello, this is your GET /spaceship response to see one singular spaceship',
        'data': single_spaceship.serialize()
    }), 200

@app.route('/spaceship', methods=['POST'])
def add_spaceship():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'You must send info in body'}), 400
    if 'name' not in body or 'crew' not in body or 'model' not in body or 'lenght' not in body or 'cargo_capacity' not in body:
        return jsonify({'msg': 'Fields "name", "crew", "model", "lenght", and "cargo_capacity" are mandatory'}), 400
    if Spaceships.query.filter_by(name=body['name']).first():
        return jsonify({'msg': 'A spaceship with this name already exists'}), 400

    new_spaceship = Spaceships(
        name=body['name'],
        crew=body['crew'],
        model=body['model'],
        lenght=body['lenght'],
        cargo_capacity=body['cargo_capacity']
    )
    
    db.session.add(new_spaceship)
    db.session.commit()

    return jsonify({
        'msg': 'New Spaceship Created!',
        'data': new_spaceship.serialize()
    }), 201

@app.route('/spaceship/<int:spaceship_id>', methods=['PUT'])
def update_spaceship(spaceship_id):
    body = request.get_json(silent=True)
    spaceship = Spaceships.query.get(spaceship_id)
    if spaceship is None:
        return jsonify({'msg': f'Spaceship with id: {spaceship_id} doesn\'t exist'}), 404
    if body is None:
        return jsonify({'msg': 'You must send info in the body'}), 400
    if 'name' not in body or 'crew' not in body or 'model' not in body or 'lenght' not in body or 'cargo_capacity' not in body:
        return jsonify({'msg': 'Fields "name", "crew", "model", "lenght", and "cargo_capacity" are mandatory'}), 400
    
    spaceship.name = body['name']
    spaceship.crew = body['crew']
    spaceship.model = body['model']
    spaceship.lenght = body['lenght']
    spaceship.cargo_capacity = body['cargo_capacity']
    
    db.session.commit()
    return jsonify({
        'msg': f'Spaceship with Id: {spaceship_id} modified!',
        'data': spaceship.serialize()
    }), 200

@app.route('/spaceship/<int:spaceship_id>', methods=['DELETE'])
def delete_spaceship(spaceship_id):
    spaceship = Spaceships.query.get(spaceship_id)
    if spaceship is None:
        return jsonify({'msg': f'Spaceship with id: {spaceship_id} doesn\'t exist'}), 404

    existing_favorites = FavoriteSpaceships.query.filter_by(spaceship_id=spaceship_id).all()
    if existing_favorites:
        return jsonify({'msg': f'Please delete the favorite relationships for spaceship with id: {spaceship_id} before deleting the spaceship'}), 400
    
    db.session.delete(spaceship)
    db.session.commit()
    
    return jsonify({'msg': f'Spaceship with id: {spaceship_id} deleted'}), 200

# Post Favorite Spaceship
@app.route('/favorite/spaceship/<int:spaceship_id>/<int:user_id>', methods=['POST'])
def add_favorite_spaceship(spaceship_id, user_id):
    user = User.query.get(user_id)
    spaceship = Spaceships.query.get(spaceship_id)
    
    if user is None:
        return jsonify({'msg': f'User with id: {user_id} doesn\'t exist'}), 404
    if user.is_active == False:
        return jsonify({'msg': f'User with id: {user_id} is deactivated'}), 409
    if spaceship is None:
        return jsonify({'msg': f'Spaceship with id: {spaceship_id} doesn\'t exist'}), 404
    
    existing_favorite = FavoriteSpaceships.query.filter_by(user_id=user_id, spaceship_id=spaceship_id).first()
    if existing_favorite:
        return jsonify({'msg': f'Spaceship with id: {spaceship_id} is already a favorite for user with id: {user_id}'}), 409
    
    new_relationship = FavoriteSpaceships(
        user_id=user_id,
        spaceship_id=spaceship_id
    )
    db.session.add(new_relationship)
    db.session.commit()

    return jsonify({'msg': f'Spaceship with id: {spaceship_id} added as favorite for user with id: {user_id}'}), 200

# Delete Favorite Spaceship
@app.route('/favorite/spaceship/<int:spaceship_id>/<int:user_id>', methods=['DELETE'])
def delete_favorite_spaceship(spaceship_id, user_id):
    user = User.query.get(user_id)
    spaceship = Spaceships.query.get(spaceship_id)
    
    if user is None:
        return jsonify({'msg': f'User with id: {user_id} doesn\'t exist'}), 404
    if user.is_active == False:
        return jsonify({'msg': f'User with id: {user_id} is deactivated'}), 409
    if spaceship is None:
        return jsonify({'msg': f'Spaceship with id: {spaceship_id} doesn\'t exist'}), 404
    
    existing_favorite = FavoriteSpaceships.query.filter_by(user_id=user_id, spaceship_id=spaceship_id).first()
    if existing_favorite is None:
        return jsonify({'msg': f'Favorite relationship between user id: {user_id} and spaceship id: {spaceship_id} doesn\'t exist'}), 404
    
    db.session.delete(existing_favorite)
    db.session.commit()

    return jsonify({'msg': f'Spaceship with id: {spaceship_id} deleted from favorites for user with id: {user_id}'}), 200


"""
CHARACTERS BELOW HERE (7 Endpoints)
"""

@app.route('/characters', methods=['GET'])
def get_all_characters():
    all_characters = Characters.query.all()
    all_characters_serialize = []
    for character in all_characters:
        all_characters_serialize.append(character.serialize())
    response_body = {
        "msg": "Hello, this is your GET /characters response to see all the characters",
        "data": all_characters_serialize
    }
    return jsonify(response_body), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_single_character(character_id):
    single_character = Characters.query.get(character_id)
    if single_character is None:
        return jsonify({'msg': f'Character with id: {character_id} doesn\'t exist'}), 404
    return jsonify({
        'msg': 'Hello, this is your GET /character response to see one singular character',
        'data': single_character.serialize()
    }), 200

@app.route('/character', methods=['POST'])
def add_character():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'You must send info in body'}), 400
    if 'name' not in body or 'skin_color' not in body or 'birth_year' not in body or 'gender' not in body or 'height' not in body:
        return jsonify({'msg': 'Fields "name", "skin_color", "birth_year", "gender", and "height" are mandatory'}), 400
    if Characters.query.filter_by(name=body['name']).first():
        return jsonify({'msg': 'A character with this name already exists'}), 400

    new_character = Characters(
        name=body['name'],
        skin_color=body['skin_color'],
        birth_year=body['birth_year'],
        gender=body['gender'],
        height=body['height']
    )
    
    db.session.add(new_character)
    db.session.commit()

    return jsonify({
        'msg': 'New Character Created!',
        'data': new_character.serialize()
    }), 201

@app.route('/character/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    body = request.get_json(silent=True)
    character = Characters.query.get(character_id)
    if character is None:
        return jsonify({'msg': f'Character with id: {character_id} doesn\'t exist'}), 404
    if body is None:
        return jsonify({'msg': 'You must send info in the body'}), 400
    if 'name' not in body or 'skin_color' not in body or 'birth_year' not in body or 'gender' not in body or 'height' not in body:
        return jsonify({'msg': 'Fields "name", "skin_color", "birth_year", "gender", and "height" are mandatory'}), 400
    
    character.name = body['name']
    character.skin_color = body['skin_color']
    character.birth_year = body['birth_year']
    character.gender = body['gender']
    character.height = body['height']
    
    db.session.commit()
    return jsonify({
        'msg': f'Character with Id: {character_id} modified!',
        'data': character.serialize()
    }), 200

@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Characters.query.get(character_id)
    if character is None:
        return jsonify({'msg': f'Character with id: {character_id} doesn\'t exist'}), 404

    db.session.delete(character)
    db.session.commit()
    
    return jsonify({'msg': f'Character with id: {character_id} deleted'}), 200

# Post Favorite Character
@app.route('/favorite/character/<int:character_id>/<int:user_id>', methods=['POST'])
def add_favorite_character(character_id, user_id):
    user = User.query.get(user_id)
    character = Characters.query.get(character_id)
    
    if user is None:
        return jsonify({'msg': f'User with id: {user_id} doesn\'t exist'}), 404
    if user.is_active == False:
        return jsonify({'msg': f'User with id: {user_id} is deactivated'}), 409
    if character is None:
        return jsonify({'msg': f'Character with id: {character_id} doesn\'t exist'}), 404
    
    existing_favorite = FavoriteCharacters.query.filter_by(user_id=user_id, character_id=character_id).first()
    if existing_favorite:
        return jsonify({'msg': f'Character with id: {character_id} is already a favorite for user with id: {user_id}'}), 409
    
    new_relationship = FavoriteCharacters(
        user_id=user_id,
        character_id=character_id
    )
    db.session.add(new_relationship)
    db.session.commit()

    return jsonify({'msg': f'Character with id: {character_id} added as favorite for user with id: {user_id}'}), 200

# Delete Favorite Character
@app.route('/favorite/character/<int:character_id>/<int:user_id>', methods=['DELETE'])
def delete_favorite_character(character_id, user_id):
    user = User.query.get(user_id)
    character = Characters.query.get(character_id)
    
    if user is None:
        return jsonify({'msg': f'User with id: {user_id} doesn\'t exist'}), 404
    if user.is_active == False:
        return jsonify({'msg': f'User with id: {user_id} is deactivated'}), 409
    if character is None:
        return jsonify({'msg': f'Character with id: {character_id} doesn\'t exist'}), 404
    
    existing_favorite = FavoriteCharacters.query.filter_by(user_id=user_id, character_id=character_id).first()
    if existing_favorite is None:
        return jsonify({'msg': f'Favorite relationship between user id: {user_id} and character id: {character_id} doesn\'t exist'}), 404
    
    db.session.delete(existing_favorite)
    db.session.commit()

    return jsonify({'msg': f'Character with id: {character_id} deleted from favorites for user with id: {user_id}'}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)