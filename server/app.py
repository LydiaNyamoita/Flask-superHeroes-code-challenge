#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate


from models import db, Power, Hero, hero_powers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'Heroes'

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



from flask import Flask, jsonify, request

# ... (Your other imports and code)

@app.route('/powers/<int:id>', methods=['PATCH'])
def patch_power_by_id(id):
    try:
        power = Power.query.filter_by(id=id).first()
        if not power:
            return jsonify({'error': 'Power not found'}), 404

        data = request.get_json()

        if 'description' in data:
            new_description = data['description']

            
            if not new_description or len(new_description) < 20:
                return jsonify({'errors': ['Description must be at least 20 characters long']}), 400

            
            power.description = new_description

            
            db.session.commit()

            
            power_data = {
                'id': power.id,
                'name': power.name,
                'description': power.description,
            }
            return jsonify(power_data), 200
        else:
            return jsonify({'error': 'Description field is required'}), 400

    except Exception as e:
        return jsonify({'errors': [str(e)]}), 500



@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    try:
        data = request.get_json()

        
        if "strength" not in data or "power_id" not in data or "hero_id" not in data:
            return jsonify({"errors": ["strength, power_id, and hero_id are required fields"]}), 400

        
        hero = Hero.query.get(data["hero_id"])
        power = Power.query.get(data["power_id"])

        
        if not hero or not power:
            return jsonify({"errors": ["Hero or Power not found"]}), 404

        
        hero_powers_association = hero_powers.insert().values(
            strength=data["strength"],
            hero_id=data["hero_id"],
            power_id=data["power_id"]
        )

        
        db.session.execute(hero_powers_association)
        db.session.commit()

        
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

        return jsonify(hero_data), 201  

    except Exception as e:
        return jsonify({"errors": [str(e)]}), 500  




if __name__ == '__main__':
    app.run(port=5555)
