from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favoritecha: Mapped[list['FavoriteCharacters']
                        ] = relationship(back_populates='user')
    favoriteveh: Mapped[list['FavoriteVehicles']
                        ] = relationship(back_populates='user', cascade="all, delete-orphan")
    favoritepla: Mapped[list['FavoritePlanets']
                        ] = relationship(back_populates='user')

    def __repr__(self):
        return f'<User {self.user_name}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "user_name": self.user_name,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }


class Characters(db.Model):
    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_name: Mapped[str] = mapped_column(String(20), nullable=True)
    specie: Mapped[str] = mapped_column(String(20), nullable=False)
    height: Mapped[int] = mapped_column(Integer)
    favorite_by: Mapped[list['FavoriteCharacters']
                        ] = relationship(back_populates='character', cascade="all, delete-orphan")
    vehicle: Mapped[list['Vehicle']] = relationship(back_populates='driver')

    def __repr__(self):
        return f'<Character {self.first_name} {self.last_name}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "specie": self.specie,
            "height": self.height,
        }


class FavoriteCharacters(db.Model):
    __tablename__ = 'favorite_characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='favoritecha')
    character_id: Mapped[int] = mapped_column(ForeignKey('character.id'))
    character: Mapped['Characters'] = relationship(
        back_populates='favorite_by')

    def __repr__(self):
        return f'{self.user} le gusta {self.character}'


class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    max_speed: Mapped[int] = mapped_column(Integer)
    driver_id: Mapped[int] = mapped_column(
        ForeignKey('character.id'), nullable=True, unique=True)
    driver: Mapped['Characters'] = relationship(back_populates='vehicle')
    favorite_by: Mapped[list['FavoriteVehicles']
                        ] = relationship(back_populates='vehicle', cascade="all, delete-orphan")
    
    def serialize(self):
        return{
            "name": self.name,
            "max_speed": self.max_speed,
            "driver_id": self.driver_id,
        }

    def __repr__(self):
        return f'<Vehicle {self.name}>'


class FavoriteVehicles(db.Model):
    __tablename__ = 'favorite_vehicles'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='favoriteveh')
    vehicle_id: Mapped[int] = mapped_column(ForeignKey('vehicle.id'))
    vehicle: Mapped['Vehicle'] = relationship(back_populates='favorite_by')

    def __repr__(self):
        return f'{self.user} le gusta {self.vehicle}>'


class Planets(db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    population: Mapped[int] = mapped_column(Integer)
    climate: Mapped[str] = mapped_column(String(250), nullable=True)
    favorite_by: Mapped[list['FavoritePlanets']
                        ] = relationship(back_populates='planet', cascade="all, delete-orphan")
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
        }

    def __repr__(self):
        return f'<Planet {self.name}>'


class FavoritePlanets(db.Model):
    __tablename__ = 'favorite_planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='favoritepla')
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'))
    planet: Mapped['Planets'] = relationship(back_populates='favorite_by')


    def __repr__(self):
        return f'{self.user} le gusta {self.planet}>'
