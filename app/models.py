from app import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import registry


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    articles = db.relationship('Articles', back_populates='user', lazy=True)
    messages = db.relationship('Message', back_populates='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"


# Modèle de catégorie
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name_categorie = db.Column(db.String(255), nullable=False)
    articles = relationship('Articles', back_populates='categorie')

    def __repr__(self):
        return f"Category('{self.name_categorie}')"

# Modèle d'article
class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)
    text = db.Column(db.String)
    titre = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    categorie = relationship('Category', back_populates='articles')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Correction : 'user.id' doit être en minuscules
    user = relationship('User', back_populates='articles')

    def __repr__(self):
        return f"Articles('{self.titre}', '{self.date}')"

# Modèle de salle
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2000), nullable=False)
    messages = db.relationship('Message', back_populates='room', lazy=True)

    def __repr__(self):
        return f"Room('{self.name}')"
        
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.today())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    # Utilisez back_populates au lieu de backref pour éviter les ambiguïtés
    user = db.relationship('User', back_populates='messages')
    room = db.relationship('Room', back_populates='messages')

    def __repr__(self):
        return f"Message('{self.value}', '{self.date}')"



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)

def __repr__(self):
        return f"Product('{self.name}', '{self.price}')"