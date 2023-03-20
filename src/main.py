"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from types import LambdaType
import requests
from flask import Flask, request, jsonify, url_for
from crypt import methods
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Starship, Vehicles, Species, Films
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpointsPPPP
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

BASE_URL = "https://www.swapi.tech/api/"


@app.route('/characters', methods=['GET'])
def populate_characters():
    characters = Character.query.all()
    return jsonify(list(map(
        lambda inst: inst.shortalize(),
        characters
    ))), 200

@app.route('/planet', methods=['GET'])
def populate_planet():
    Planet = Planet.query.all()
    return jsonify(list(map(
        lambda planet: planet.shortalize(),
        Planet
    ))), 200

@app.route('/starship', methods=['GET'])
def populate_starship():
    Starship = Starship.query.all()
    return jsonify(list(map(
        lambda Starship: Starship.shortalize(),
        Starship
    ))), 200

@app.route('/vehicles', methods=['GET'])
def populate_vehicles():
    Vehicles = Vehicles.query.all()
    return jsonify(list(map(
        lambda Vehicles: Vehicles.shortalize(),
        Vehicles
    ))), 200

@app.route('/species', methods=['GET'])
def populate_species():
    Species = Species.query.all()
    return jsonify(list(map(
        lambda Species: Species.shortalize(),
        Species
    ))), 200

@app.route('/films', methods=['GET'])
def populate_films():
    Films = Films.query.all()
    return jsonify(list(map(
        lambda Films: Films.shortalize(),
        Films
    ))), 200

 
@app.route('/populatedb', methods=["POST"])
def populate_db(amount=1):
    for (swapi_end, resource) in [
        # ('/people', 'character'),
        #('/planets', 'planet'),
        ('/starships', 'starship')
    ]:
        populate_items(swapi_end, resource, amount)
    
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

def populate_items(swapi_end, resource, amount):
    print(f"starting {resource}s requests")
    response = requests.get(
        f"{BASE_URL}{swapi_end}"
    )
    results = response.json()['results']
    all_items = []
    for result in results:
        id = result['uid']
        response = requests.get(result['url'])
        properties = response.json()['result']['properties']
        properties['id'] = int(id)
        all_items.append(properties)
    items = []
    
    print(f"creating {resource}s instances")
    for item in all_items:
        item_instance = None
        
        if resource == "character":
            item_instance = Character.create(item)
        elif resource == "planet":
            item_instance = Planet.create(item)
        elif resource == "starship":
            item_instance = Starship.create(item)
        elif resource == "vehicle":
            item_instance = Vehicles.create(item)
        elif resource == "specie":
            item_instance = Species.create(item)
        else:
            item_instance = Films.create(item)
        if item_instance is None: continue
        items.append(item_instance)
    print(f"created {len(items)} {resource}s")


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
