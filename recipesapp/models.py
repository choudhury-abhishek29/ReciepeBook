from . import db, ma
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    userhash = db.Column(db.String(100))
    email = db.Column(db.String(50))
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    recipes = db.relationship('Recipe', backref='author', lazy=True)

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "username", "email")


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), db.ForeignKey('user.username'), nullable=False)
    recipename = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(500), nullable=False)
    instructions = db.Column(db.String(500))
    servingsize = db.Column(db.Integer)
    category = db.Column(db.String(20))
    notes = db.Column(db.String(100))
    dateposted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    datemodified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

class RecipeSchema(ma.Schema):
    class Meta:
        fields = ("id", "recipename", "ingredients", "instructions", "servingsize", "category", "notes",
                  "dateposted", "datemodified")
