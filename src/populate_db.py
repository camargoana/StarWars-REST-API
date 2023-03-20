from email.policy import default
import click
import requests
from models import Character, Planet, Starship, Vehicles, Species, Films
from flask import Flask, current_app as app, jsonify

BASE_URL = "https://www.swapi.tech/api"

# @app.cli.command("populate-db")
# @click.argument('amount', type=click.INT, default=1)
def populate_db(amount=1):
    for (swapi_end, resource) in [
        ('/people', 'character'),
        ('/planets', 'planet'),
        ('/starships', 'starship'),
        ('/vehicles', 'vehicle'),
        ('/species', 'specie'),
        ('/films', 'film')
    ]:
        populate_items(swapi_end, resource, amount)

def populate_items(swapi_end, resource, amount):
    print(f"starting {resource}s requests")
    response = requests.get(
        f"{BASE_URL}{swapi_end}/?page=1&limit={amount}"
    )
    results = response.json()['results']
    all_items = []
    for result in results:
        response = requests.get(result['url'])
        properties = response.json()['result']['properties']
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



populate_db(1)
