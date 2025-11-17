# models/user.py
from utils.database import db
from datetime import datetime
import bcrypt

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Preferences stored as JSON
    preferences = db.Column(db.JSON, default={
        'theme': 'default',
        'hint_frequency': 50,
        'auto_hints': False,
        'smart_hints': True,
        'community_tips': True
    })
    
    # Relationship to games (one-to-many)
    # backref creates a 'user' attribute on Game model
    games = db.relationship('Game', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')
    
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'), 
            self.password_hash.encode('utf-8')
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'preferences': self.preferences,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }