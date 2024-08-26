"""
CLASSES
"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name =  db.Column(db.String(35), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'User con id: {self.id} y email: {self.email}'

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    planet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    diameter = db.Column(db.Integer, nullable=True)
    population = db.Column(db.Integer, nullable=True)
    duration_day = db.Column(db.Integer, nullable=True)
    terrain = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'Planet with name: {self.name}'

    def serialize(self):
        return {
            "planet_id": self.planet_id,
            "name": self.name,
            "diameter": self.diameter,
            "population": self.population,
            "terrain": self.terrain,
            "duration_day": self.duration_day
        }
    
class Spaceships(db.Model):
    __tablename__ = 'spaceships'
    spaceship_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    crew = db.Column(db.Integer, nullable=True)
    model = db.Column(db.String(50), nullable=True)
    lenght = db.Column(db.Integer,  nullable=True)
    cargo_capacity = db.Column(db.Integer,  nullable=True)

    def __repr__(self):
        return f'Spaceship with name: {self.name}'

    def serialize(self):
        return {
            "spaceship_id": self.spaceship_id,
            "name": self.name,
            "crew": self.crew,
            "lenght": self.lenght,
            "model": self.model,
            "cargo_capacity": self.cargo_capacity
        }  
      
class Characters(db.Model):
    __tablename__ = 'characters'
    character_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    skin_color = db.Column(db.String(30), nullable=True) 
    birth_year = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    height = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'Character with name: {self.name}'

    def serialize(self):
        return {
            "character_id": self.character_id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "skin_color": self.skin_color
        }    

class FavoritePlanets(db.Model):
    __tablename__ = 'favorite_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    user_relationship = db.relationship('User', backref='favorite_planets')
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.planet_id'), nullable=False)  
    planet_relationship = db.relationship('Planets', backref='favorite_planets')

    def __repr__(self):
        return f'(User: {self.user_id} likes planet {self.planet_id})'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }
    
class FavoriteCharacters(db.Model):
    __tablename__ = 'favorite_characters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    user_relationship = db.relationship('User', backref='favorite_characters')
    character_id = db.Column(db.Integer, db.ForeignKey('characters.character_id'), nullable=False) 
    character_relationship = db.relationship('Characters', backref='favorite_characters')

    def __repr__(self):
        return f'(User: {self.user_id} likes character {self.character_id})'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }
    
class FavoriteSpaceships(db.Model):

    __tablename__ = 'favorite_spaceships'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    user_relationship = db.relationship('User', backref='favorite_spaceships')
    spaceship_id = db.Column(db.Integer, db.ForeignKey('spaceships.spaceship_id'), nullable=False)  
    spaceship_relationship = db.relationship('Spaceships', backref='favorite_spaceships')

    def __repr__(self):
        return f'(User: {self.user_id} likes spaceship {self.spaceship_id})'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "spaceship_id": self.spaceship_id
        }