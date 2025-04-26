from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    birth_year = db.Column(db.String(32))
    eye_color = db.Column(db.String(32))
    gender = db.Column(db.String(32))
    hair_color = db.Column(db.String(32))
    height = db.Column(db.String(8))
    mass = db.Column(db.String(32))
    homeworld = db.Column(db.String(128))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'birth_year': self.birth_year,
            'eye_color': self.eye_color,
            'gender': self.gender,
            'hair_color': self.hair_color,
            'height': self.height,
            'mass': self.mass,
            'homeworld': self.homeworld
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    climate = db.Column(db.String(32))
    diameter = db.Column(db.String(16))
    gravity = db.Column(db.String(8))
    orbital_period = db.Column(db.String(8))
    population = db.Column(db.String(16))
    rotation_period = db.Column(db.String(8))
    surface_water = db.Column(db.String(3))
    terrain = db.Column(db.String(32))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'climate': self.climate,
            'diameter': self.diameter,
            'gravity': self.gravity,
            'orbital_period': self.orbital_period,
            'population': self.population,
            'rotation_period': self.rotation_period,
            'surface_water': self.surface_water,
            'terrain': self.terrain
        }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(32))
    favorites = db.relationship('Favorites', backref='user', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username
        }

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)

    people = db.relationship('People', lazy=True)
    planet = db.relationship('Planets', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'people_id': self.people_id,
            'planets_id': self.planets_id
        }
