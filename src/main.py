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
from models import db, User,Planets,People,Favorites,Starships
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

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# GET requets

@app.route('/user', methods=["GET"])
def user_list ():
    users = User.query.all()
    request_body = list(map(lambda user:user.serialize(),users))
    return jsonify(request_body),200

@app.route('/people', methods=["GET"])
def people_list ():
    peoples = People.query.all()
    request_body = list(map(lambda people:people.serialize(),peoples))
    return jsonify(request_body),200

@app.route('/people/<id>', methods=["GET"])
def single_people(id):
    people = People.query.filter_by(id=id).first()
    if people is None:
        return APIException("No se encontro el character",status_code=404)
    request_body = people.serialize()
    return jsonify(request_body),200

@app.route('/planets', methods=["GET"])
def planets_list ():
    planets = Planets.query.all()
    request_body = list(map(lambda planets:planets.serialize(),planets))
    return jsonify(request_body),200

@app.route('/planets/<id>', methods=["GET"])
def single_planet(id):
    planet = Planets.query.filter_by(id=id).first()
    if planet is None:
        return APIException("No se encontro el planeta",status_code=404)
    request_body = planet.serialize()
    return jsonify(request_body),200

@app.route('/starships', methods=["GET"])
def starships_list ():
    starships = Starships.query.all()
    request_body = list(map(lambda starships:starships.serialize(),starships))
    return jsonify(request_body),200

@app.route('/starships/<id>', methods=["GET"])
def single_starship(id):
    starship = Starships.query.filter_by(id=id).first()
    if starship is None:
        return APIException("No se encontro el planeta",status_code=404)
    request_body = starship.serialize()
    return jsonify(request_body),200
    
# POST requests

@app.route('/user', methods=["POST"])
def user_post ():
    data = request.get_json()
    user = User(user_name=data["user_name"],first_name=data["first_name"],last_name=data["last_name"],email=data["email"],password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify("Message : Se adiciono el usuario!"),200
    return jsonify(request_body),200

@app.route('/people', methods=["POST"])
def people_post ():
    data = request.get_json()
    people = People(name=data["name"],height=data["height"],mass=data["mass"],hair_color=data["hair_color"],skin_color=data["skin_color"],eye_color=data["eye_color"],birth_year=data["birth_year"],gender=data["gender"],created=data["created"],edited=data["edited"],homeworld=data["homeworld"],url=data["url"])
    db.session.add(people)
    db.session.commit()
    return jsonify("Message : Se adiciono el personaje!"),200
    return jsonify(request_body),200

@app.route('/planets', methods=["POST"])
def planet_post ():
    data = request.get_json()
    planets = Planets(name=data["name"],population=data["population"],terrain=data["terrain"],diameter=data["diameter"],rotation_period=data["rotation_period"],orbital_period=data["orbital_period"],gravity=data["gravity"],climate=data["climate"],surface_water=data["surface_water"],created=data["created"],edited=data["edited"],url=data["url"])
    db.session.add(planets)
    db.session.commit()
    return jsonify("Message : Se adiciono el planeta!"),200
    return jsonify(request_body),200

@app.route('/starships', methods=["POST"])
def starships_post ():
    data = request.get_json()
    starships = Starships(name=data["name"],model=data["model"],starship_class=data["starship_class"],manufacturer=data["manufacturer"],length=data["length"],crew=data["crew"],passengers=data["passengers"],MGLT=data["MGLT"],cargo_capacity=data["cargo_capacity"],consumables=data["consumables"],url=data["url"])
    db.session.add(starships)
    db.session.commit()
    return jsonify("Message : Se adiciono la nave!"),200
    return jsonify(request_body),200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
