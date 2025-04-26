import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, People, Planets

app = Flask(__name__)
app.url_map.strict_slashes = False
db_url = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://") if db_url else "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Migrate(app, db)
db.init_app(app)
CORS(app)

@app.route('/people', methods=['GET'])
def list_people():
    return jsonify([p.serialize() for p in People.query.all()]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    p = People.query.get_or_404(people_id)
    return jsonify(p.serialize()), 200

@app.route('/people', methods=['POST'])
def create_person():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({"error": "El campo 'name' es obligatorio"}), 400
    p = People(
        name=data['name'],
        birth_year=data.get('birth_year'),
        eye_color=data.get('eye_color'),
        gender=data.get('gender'),
        hair_color=data.get('hair_color'),
        height=data.get('height'),
        mass=data.get('mass'),
        homeworld=data.get('homeworld')
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.serialize()), 201

@app.route('/people/<int:people_id>', methods=['PUT'])
def update_person(people_id):
    p = People.query.get_or_404(people_id)
    data = request.get_json() or {}
    if 'name' in data and not data['name']:
        return jsonify({"error": "El campo 'name' no puede quedar vacío"}), 400
    for field in ['name','birth_year','eye_color','gender','hair_color','height','mass','homeworld']:
        if field in data:
            setattr(p, field, data[field])
    db.session.commit()
    return jsonify(p.serialize()), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    p = People.query.get_or_404(people_id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"msg": f"Person {people_id} eliminada"}), 200

@app.route('/planets', methods=['GET'])
def list_planets():
    return jsonify([pl.serialize() for pl in Planets.query.all()]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    pl = Planets.query.get_or_404(planet_id)
    return jsonify(pl.serialize()), 200

@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({"error": "El campo 'name' es obligatorio"}), 400
    pl = Planets(
        name=data['name'],
        climate=data.get('climate'),
        diameter=data.get('diameter'),
        gravity=data.get('gravity'),
        orbital_period=data.get('orbital_period'),
        population=data.get('population'),
        rotation_period=data.get('rotation_period'),
        surface_water=data.get('surface_water'),
        terrain=data.get('terrain')
    )
    db.session.add(pl)
    db.session.commit()
    return jsonify(pl.serialize()), 201

@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    pl = Planets.query.get_or_404(planet_id)
    data = request.get_json() or {}
    if 'name' in data and not data['name']:
        return jsonify({"error": "El campo 'name' no puede quedar vacío"}), 400
    for field in ['name','climate','diameter','gravity','orbital_period','population','rotation_period','surface_water','terrain']:
        if field in data:
            setattr(pl, field, data[field])
    db.session.commit()
    return jsonify(pl.serialize()), 200

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    pl = Planets.query.get_or_404(planet_id)
    db.session.delete(pl)
    db.session.commit()
    return jsonify({"msg": f"Planet {planet_id} eliminada"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
