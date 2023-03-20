from email.mime import image
from turtle import title
from venv import create
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
from flask.cli import main


db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created = db.Column(db.DateTime(timezone=True), default=db.func.now())
    updated = db.Column(db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now())

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(120),unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Item(Base):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    nature = db.Column(db.String(20), nullable=False, default='item')

    def __repr__(self) -> str:
        return f"{self.id}: {self.nature}"

    def __init__(self, *args, **kwargs): # keyword arguments
        for (key, value) in kwargs.items(): #
            if key in ('created', 'updated', 'nature'): continue
            if hasattr(self, key): #
                attribute_type = getattr(self.__class__, key).type
                try:
                    attribute_type.python_type(value)
                    setattr(self, key, value) #

                except Exception as error:
                    print("ignoring key ", key, " with ", value, " for ", attribute_type.python_type, " because ", error.args)

    @classmethod
    def create(cls, data):
        # crear la instancia
        instance = cls(**data)
        if (not isinstance(instance, cls)): 
            print("FALLA EL CONSTRUCTOR")
            return None
        # guardar en bdd
        db.session.add(instance)
        try:
            db.session.commit()
            print(f"created: {instance.nature}")
            return instance
        except Exception as error:
            db.session.rollback()
            raise Exception(error.args)

class Character(Item):
    __tablename__ = 'character'
    height = db.Column(db.String(80), nullable=False)
    mass = db.Column(db.String(80), nullable=False)
    hair_color = db.Column(db.String(80), nullable=False)
    skin_color = db.Column(db.String(80), nullable=False)
    eye_color = db.Column(db.String(80), nullable=False)
    birth_year = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    homeworld = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(80), nullable=False)
    nature = db.Column(db.String(20), nullable=False, default='character')

    def __repr__(self) -> str:
        return f"{self.id}: {self.name}, {self.homeworld}, {self.eye_color}"

    def serialize(self):
        return{
            "id": self.id,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender" : self.gender,
            "name"    : self.name,
            "homeworld" : self.homeworld,
            "url"   : self.url
        }

    def shortalize(self):
        """
            devuelve un diccionario que represetna al objeto
            para poder convertirlo en json y responder al front end
        """
        return {
            "id": self.id,
            "name": self.name,
            "homeworld": self.homeworld,
            "url": f"http://127.0.0.1:3000/characters/{self.id}"
        }

class Planet(Item):
    terrain = db.Column(db.String(),nullable=False)
    climate = db.Column(db.String(), nullable=False)
    population = db.Column(db.String(),nullable=False)
    diameter = db.Column(db.String(80), nullable=False)
    orbital_period = db.Column(db.String(100), nullable=False)
    rotation_period = db.Column(db.String(80), nullable=False)
    gravity = db.Column(db.String(80), nullable=False)
    surface_water = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(80), nullable=False)
    nature = db.Column(db.String(20), nullable=False, default='planet')

    def serialize(self):
        return{
            "id": self.id,
            "terrain": self.terrain,
            "climate": self.climate,
            "population": self.population,
            "diameter": self.diameter,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "gravity" : self.gravity,
            "surface_water" : self.surface_water,
            "name": self.name,
            "url": self.url
        }

    def shortalize(self):
        """
            devuelve un diccionario que represetna al objeto
            para poder convertirlo en json y responder al front end
        """
        return {
            "id": self.id,
            "name": self.name,
            "url": f"http://127.0.0.1:3000/planet/{self.id}"
        }

class Starship(Item):
    cargo_capacity = db.Column(db.String(), nullable=False)
    starship_class = db.Column(db.String(), nullable=False)
    consumables = db.Column(db.String(100), nullable=False)
    manufacturer= db.Column(db.String(80), nullable=False)
    length = db.Column(db.String(), nullable=False)
    crew = db.Column(db.String(),nullable=False)
    passengers = db.Column(db.String() , nullable=False)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(80), nullable=False)
    nature = db.Column(db.String(20), nullable=False, default='starship')
    
    def serialize(self):
        return{
            "id": self.id,
            "cargo_capacity": self.cargo_capacity,
            "starships_class": self.starships_class,
            "consumables": self.consumables,
            "manufacturer": self.manufacturer,
            "length": self.length,
            "crew": self.crew,
            "passengers" : self.passengers,
        }

    def shortalize(self):
        """
            devuelve un diccionario que represetna al objeto
            para poder convertirlo en json y responder al front end
        """
        return {
            "id": self.id,
            "name": self.name,
            "url": f"http://127.0.0.1:3000/starship/{self.id}"
        }

class Vehicles(Item):
    model = db.Column(db.String(80), nullable=False)
    vehicle_class = db.Column(db.String(80), nullable=False)
    manufaturer = db.Column(db.String(80), nullable=False)
    cost_in_credits = db.Column(db.String(80), nullable=False)
    passengers= db.Column(db.String(80), nullable=False)
    cargo_capacity= db.Column(db.String(10), nullable=False)
    length = db.Column(db.String(80), nullable=False)
    consumables= db.Column(db.String(100), nullable=False)
    passengers = db.Column(db.String(80),nullable=False)
    max_atmosfering_speed = db.Column(db.String(80), nullable=False)
    crew = db.Column(db.String(80),nullable=False)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(80), nullable=False)
    nature = db.Column(db.String(20), nullable=False, default='vehicle')

    def serialize(self):
        return{
            "id": self.id,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufaturer": self.manufaturer,
            "cost_in_credits": self.cost_in_credits,
            "passengers": self.passengers,
            "max_atmosfering_speed": self.max_atmosfering_speed,
            "crew" : self.crew,
            "name" : self.name,
            "url " : self.url ,
        }

class Species(Item):
    lifespan = db.Column(db.String())
    height = db.Column(db.String())
    skin_color = db.Column(db.String(80), nullable=False)
    eye_color = db.Column(db.String(80), nullable=False)
    classification = db.Column(db.String(80), nullable=False)
    designation = db.Column(db.String(80), nullable=False)
    language = db.Column(db.String(10), nullable=False)
    homeworld = db.Column(db.String(80), nullable=False)
    nature = db.Column(db.String(20), nullable=False, default='specie')

    def serialize(self):
        return{
            "id": self.id,
            "lifespan": self.lifespan,
            "height": self.height,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "classification": self.classification,
            "designation": self.designation,
            "language" : self.language,
            "homeworld " : self.created,
        }
    
class Films(Item):
    episode_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    opening_crawl = db.Column(db.String(80), nullable=False)
    director = db.Column(db.String(80), nullable=False)
    producer = db.Column(db.String(80), nullable=False)
    nature = db.Column(db.String(20), nullable=False, default='film')


    def serialize(self):
        return{
            "episode_id": self.episode_id,
            "title": self.title,
            "opening_crawl": self.opening_crawl,
            "director": self.director,
            "producer": self.producer,
        }
