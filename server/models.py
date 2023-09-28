from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

hero_powers = db.Table(
    'hero_powers',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('strength', db.String),
    db.Column('created_at', db.DateTime, server_default=db.func.now()),
    db.Column('updated_at', db.DateTime, onupdate=db.func.now()),
    db.Column('hero_id', db.Integer, db.ForeignKey('heros.id'), primary_key=True),
    db.Column('power_id', db.Integer, db.ForeignKey('powers.id'), primary_key=True)
)

@validates('strength')
def validate_strength(self, key, strength):
    if strength not in ('Strong', 'Weak', 'Average'):
        raise ValueError('Strength should either be Strong, Weak, or Average')
    return strength

class Hero(db.Model):
    __tablename__ = 'heros'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    powers = db.relationship('Power', secondary=hero_powers, backref='heroes')

class Power(db.Model):
    __tablename__ = 'powers'  # Corrected the typo here

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    def __repr__(self):  # Corrected the typo in __repr__
        return f"Name: {self.name}, Description: {self.description}"

    @validates('description')
    def validate_description(self, key, description):  # Corrected the typo in the function name
        if not description or len(description) < 20:
            raise ValueError("Description cannot be null or less than 20 characters.")
        return description
