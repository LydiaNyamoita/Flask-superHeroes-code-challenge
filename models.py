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
def validate_strength(self,key,strength):
    if strength not in ('Strong','Weak','Average'):
        raise ValueError('Strength should either be Strong,Weak orAverage')
    return strength


class Hero(db.Model):
    __tablename__ = 'heros'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    powers = db.relationship('Power', secondary=hero_powers, backref='heroes')



''''class HeroPower(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_id = db.Column(db.Integer, db.ForeignKey('heros.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))'''




class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    @validates('description')
    def validate_descriprion(self,key,description):
        if not description or len(description) < 20:
            raise ValueError("Description cannot be null or less than 20 characters. ")
        return description





   

    