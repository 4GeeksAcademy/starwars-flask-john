"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Vehicle, FavoriteCharacters, FavoritePlanets, FavoriteVehicles
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

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_serialized=[]
    for user in users:
        users_serialized.append(user.serialize())
    return jsonify({'data': users_serialized})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    user= User.query.get(user_id)
    if user is None:
        return jsonify({"msg":"User no existe"}), 404
    return jsonify(user.serialize()), 200

@app.route('/users', methods=['POST'])
def add_user():
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({"msg":"El body no puede estar vacio"}), 400
    if 'email' not in body:
        return jsonify({"msg":"El email es necesario"}), 400
    if 'password' not in body:
        return jsonify({"msg":"La password es necesaria"}), 400
    new_user=User()
    new_user.email=body['email']
    new_user.password=body['password']
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user= User.query.get(user_id)
    if user is None:
        return jsonify({"msg":"User no existe"}), 404
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({"msg":"El body no puede estar vacio"}), 400
    if 'user_name' in body:
        user.user_name=body['user_name']
    if 'email' in body:
        user.email=body['email']
    if 'password' in body:
        user.password=body['password']
    db.session.commit()
    return jsonify(user.serialize()), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user= User.query.get(user_id)
    if user is None:
        return jsonify({"msg":"User no existe"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg":"User eliminado"}), 200

@app.route('/people', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    characters_serialized=[]
    for character in characters:
        characters_serialized.append(character.serialize())
    return jsonify({'data': characters_serialized})

@app.route('/people/<int:character_id>', methods=['GET'])
def get_character_id(character_id):
    character= Characters.query.get(character_id)
    if character is None:
        return jsonify({"msg":"Personaje no existe"}), 404
    return jsonify(character.serialize()), 200

@app.route('/people', methods=['POST'])
def add_character():
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({"msg":"El body no puede estar vacio"}), 400
    if 'first_name' not in body:
        return jsonify({"msg":"El nombre es necesario"}), 400
    if 'specie' not in body:
        return jsonify({"msg":"La especie es necesaria"}), 400
    new_character=Characters()
    new_character.first_name=body['first_name']
    new_character.last_name=body.get('last_name')
    new_character.specie=body['specie']
    new_character.height=body.get('height')
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201

@app.route('/people/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    character= Characters.query.get(character_id)
    if character is None:
        return jsonify({"msg":"Personaje no existe"}), 404
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({"msg":"El body no puede estar vacio"}), 400
    if 'first_name' in body:
        character.first_name=body['first_name']
    if 'last_name' in body:
        character.last_name=body['last_name']
    if 'specie' in body:
        character.specie=body['specie']
    if 'height' in body:
        character.height=body['height']
    db.session.commit()
    return jsonify(character.serialize()), 200

@app.route('/people/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character= Characters.query.get(character_id)
    if character is None:
        return jsonify({"msg":"Personaje no existe"}), 404
    db.session.delete(character)
    db.session.commit()
    return jsonify({"msg":"Personaje eliminado"}), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets= Planets.query.all()
    planets_serialized=[]
    for planet in planets:
        planets_serialized.append(planet.serialize())
    return jsonify({'data':planets_serialized})

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planets_id(planet_id):
    planet= Planets.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': "Planeta no existe"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/planets', methods=['POST'])
def add_planet():
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({"msg":"El body no puede estar vacio"}), 400
    if 'name' not in body:
        return jsonify({"msg":"El nombre es necesario"}), 400
    new_planet=Planets()
    new_planet.name=body['name']
    new_planet.population=body.get('population')
    new_planet.climate=body.get('climate')
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    planet= Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"msg":"Planeta no existe"}), 404
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({"msg":"El body no puede estar vacio"}), 400
    if 'name' in body:
        planet.name=body['name']
    if 'population' in body:
        planet.population=body['population']
    if 'climate' in body:
        planet.climate=body['climate']
    db.session.commit()
    return jsonify(planet.serialize()), 200

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet= Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"msg":"Planeta no existe"}), 404
    db.session.delete(planet)
    db.session.commit()
    return jsonify({"msg":"Planeta eliminado"}), 200

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles=Vehicle.query.all()
    vehicles_serialized=[]
    for vehicle in vehicles:
        vehicles_serialized.append(vehicle.serialize())
    return jsonify({'data':vehicles_serialized})

@app.route('/vehicles/<int:vehicles_id>', methods=['GET'])
def get_vehicles_id(vehicles_id):
    vehicle= Vehicle.query.get(vehicles_id)
    if vehicle is None:
        return jsonify ({'msg': "Vehiculo no existe"}), 400
    return jsonify(vehicle.serialize()), 200

@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({"msg":"El body no puede estar vacio"}), 400
    if 'name' not in body:
        return jsonify({"msg":"El nombre es necesario"}), 400
    new_vehicle=Vehicle()
    new_vehicle.name=body['name']
    new_vehicle.max_speed=body.get('max_speed')
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify(new_vehicle.serialize()), 201

@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    vehicle= Vehicle.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({"msg":"Vehiculo no existe"}), 404
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({"msg":"El body no puede estar vacio"}), 400
    if 'name' in body:
        vehicle.name=body['name']
    if 'max_speed' in body:
        vehicle.max_speed=body['max_speed']
    db.session.commit()
    return jsonify(vehicle.serialize()), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle= Vehicle.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({"msg":"Vehiculo no existe"}), 404
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"msg":"Vehiculo eliminado"}), 200

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg":f"El Usuario con id {user_id} no existe"}), 404
    favorite_characters=[]
    favorite_vehicles=[]
    favorite_planets=[]
    for favorite_character in user.favoritecha:
        favorite_characters.append(favorite_character.character.serialize())
    for favorite_vehicle in user.favoriteveh:
        favorite_vehicles.append(favorite_vehicle.vehicle.serialize())
    for favorite_planet in user.favoritepla:
        favorite_planets.append(favorite_planet.planet.serialize())
    return jsonify({
        "favorite_characters": favorite_characters,
        "favorite_vehicles": favorite_vehicles,
        "favorite_planets": favorite_planets}), 200

@app.route('/user/<int:user_id>/favorites/people', methods=['POST'])
def add_user_favorite_characters(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg":f"El Usuario con id {user_id} no existe"}), 404
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({"msg":"El body no puede estar vacio"}), 400
    if 'character_id' in body:
        character= Characters.query.get(body['character_id'])
        if character is None:
            return jsonify({"msg":f"El Personaje con id {body['character_id']} no existe"}), 404
        new_favorite_character= FavoriteCharacters()
        new_favorite_character.user_id=user.id
        new_favorite_character.character_id=character.id
        db.session.add(new_favorite_character)
        db.session.commit()
        return jsonify({"msg":f"Personaje {character.first_name} agregado a favoritos"}), 201

@app.route('/user/<int:user_id>/favorites/vehicles', methods=['POST'])
def add_user_favorite_vehicles(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg":f"El Usuario con id {user_id} no existe"}), 404
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({"msg":"El body no puede estar vacio"}), 400
    if 'vehicle_id' in body:
        vehicle= Vehicle.query.get(body['vehicle_id'])
        if vehicle is None:
            return jsonify({"msg":f"El Vehiculo con id {body['vehicle_id']} no existe"}), 404
        new_favorite_vehicle= FavoriteVehicles()
        new_favorite_vehicle.user_id=user.id
        new_favorite_vehicle.vehicle_id=vehicle.id
        db.session.add(new_favorite_vehicle)
        db.session.commit()
        return jsonify({"msg":f"Vehiculo {vehicle.name} agregado a favoritos"}), 201

@app.route('/user/<int:user_id>/favorites/planets', methods=['POST'])
def add_user_favorite_planets(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg":f"El Usuario con id {user_id} no existe"}), 404
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({"msg":"El body no puede estar vacio"}), 400
    if 'planet_id' in body:
        planet= Planets.query.get(body['planet_id'])
        if planet is None:
            return jsonify({"msg":f"El Planeta con ID {body['planet_id']} no existe"}), 404
        new_favorite_planet= FavoritePlanets()
        new_favorite_planet.user_id=user.id
        new_favorite_planet.planet_id=planet.id
        db.session.add(new_favorite_planet)
        db.session.commit()
        return jsonify({"msg":f"Planeta {planet.name} agregado a favoritos"}), 201
    
@app.route('/user/<int:user_id>/favorites/people/<int:favorite_id>', methods=['DELETE'])
def delete_user_favorite_character(user_id, favorite_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg":f"El Usuario con ID {user_id} no existe"}), 404
    favorite_character = FavoriteCharacters.query.get(favorite_id)
    if favorite_character is None:
        return jsonify({"msg":f"No tienes un personaje favorito con ID {favorite_id}"}), 404
    db.session.delete(favorite_character)
    db.session.commit()
    return jsonify({"msg":"Personaje eliminado de favoritos"}), 200

@app.route('/user/<int:user_id>/favorites/vehicles/<int:favorite_id>', methods=['DELETE'])
def delete_user_favorite_vehicle(user_id, favorite_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg":f"El Usuario con ID {user_id} no existe"}), 404
    favorite_vehicle = FavoriteVehicles.query.get(favorite_id)
    if favorite_vehicle is None:
        return jsonify({"msg":f"No tienes un vehiculo favorito con ID {favorite_id}"}), 404
    db.session.delete(favorite_vehicle)
    db.session.commit()
    return jsonify({"msg":"Vehiculo eliminado de favoritos"}), 200

@app.route('/user/<int:user_id>/favorites/planets/<int:favorite_id>', methods=['DELETE'])
def delete_user_favorite_planet(user_id, favorite_id):  
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg":f"El Usuario con ID {user_id} no existe"}), 404
    favorite_planet = FavoritePlanets.query.get(favorite_id)
    if favorite_planet is None:
        return jsonify({"msg":f"No tienes un planeta favorito con ID {favorite_id}"}), 404
    db.session.delete(favorite_planet)
    db.session.commit()
    return jsonify({"msg":"Planeta eliminado de favoritos"}), 200
# this only runs if `$ python src/app.py` is executed


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
