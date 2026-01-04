import os
from flask_admin import Admin
from models import db, User, Characters, FavoriteCharacters, Vehicle, FavoriteVehicles, FavoritePlanets, Planets
from flask_admin.contrib.sqla import ModelView

class UserModelView(ModelView):
    column_auto_select_related = True
    column_list = ('id', 'user_name', 'email', 'is_active', 'favoritecha', 'favoriteveh', 'favoritepla')

class CharacterModelView(ModelView):
    column_auto_select_related = True
    column_list = ('id', 'first_name', 'last_name', 'specie', 'height', 'favorite_by', 'vehicle')

class FavoriteCharacterModelView(ModelView):
    column_auto_select_related = True
    column_list = ('id', 'user', 'character')

class VehicleModelView(ModelView):
    column_auto_select_related = True
    column_list = ('id', 'name', 'max_speed', 'driver', 'favorite_by')

class FavoriteVehicleModelView(ModelView):
    column_auto_select_related = True
    column_list = ('id', 'user', 'vehicle')

class PlanetModelView(ModelView):
    column_auto_select_related = True
    column_list = ('id', 'name', 'population', 'climate', 'favorite_by')

class FavoritePlanetModelView(ModelView):
    column_auto_select_related = True
    column_list = ('id', 'user', 'planet')

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(CharacterModelView(Characters, db.session))
    admin.add_view(FavoriteCharacterModelView(FavoriteCharacters, db.session))
    admin.add_view(VehicleModelView(Vehicle, db.session))
    admin.add_view(FavoriteVehicleModelView(FavoriteVehicles, db.session))
    admin.add_view(PlanetModelView(Planets, db.session))
    admin.add_view(FavoritePlanetModelView(FavoritePlanets, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))