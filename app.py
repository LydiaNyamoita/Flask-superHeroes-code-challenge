#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Power, Hero, hero_powers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, resources={r"/api/*": {"origins": "http://localhost:4000", "methods": ["GET", "POST"], "allow_headers": ["Content-Type"]}})

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'ygyuhij8y9uioipo'

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_data = [
        {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        }
        for hero in heroes
    ]
    return jsonify(hero_data)

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.filter_by(id=id).first()
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404

    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': [
            {
                'id': power.id,
                'name': power.name,
                'description': power.description
            }
            for power in hero.powers
        ]
    }
    return jsonify(hero_data)

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_data = [
        {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        for power in powers
    ]
    return jsonify(power_data)

@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.filter_by(id=id).first()
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    power_data = {
        'id': power.id,
        'name': power.name,
        'description': power.description,

    }
    return jsonify(power_data)



@app.route('/powers/<int:id>', methods=['PATCH'])
def patch_power_by_id(id):
    power = Power.query.filter_by(id=id).first()
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    
    for attr in request.json:
        setattr(power, attr,request.json.get(attr))

        db.session.add(power)
        db.session.commit()
    
    power_data = {
        'id': power.id,
        'name': power.name,
        'description': power.description,

    }
    return jsonify(power_data)



@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    try:
        data = request.get_json()

        # Check if the required fields are present in the request data
        if "strength" not in data or "power_id" not in data or "hero_id" not in data:
            return jsonify({"errors": ["strength, power_id, and hero_id are required fields"]}), 400

        # Retrieve the Hero and Power objects based on the provided IDs
        hero = Hero.query.get(data["hero_id"])
        power = Power.query.get(data["power_id"])

        # Check if the Hero and Power exist
        if not hero or not power:
            return jsonify({"errors": ["Hero or Power not found"]}), 404

        # Create a new HeroPower association
        hero_powers_association = hero_powers.insert().values(
            strength=data["strength"],
            hero_id=data["hero_id"],
            power_id=data["power_id"]
        )

        # Add the HeroPower association to the database
        db.session.execute(hero_powers_association)
        db.session.commit()

        # Fetch the updated Hero data including associated Powers
        updated_hero = Hero.query.get(data["hero_id"])
        hero_data = {
            "id": updated_hero.id,
            "name": updated_hero.name,
            "super_name": updated_hero.super_name,
            "powers": [
                {
                    "id": power.id,
                    "name": power.name,
                    "description": power.description
                }
                for power in updated_hero.powers
            ]
        }

        return jsonify(hero_data), 201  # 201 Created status code for successful creation

    except Exception as e:
        return jsonify({"errors": [str(e)]}), 500  # Handle any unexpected errors




if __name__ == '__main__':
    app.run(port=5555)
