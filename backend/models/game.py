# models/game.py
from utils.database import db
from datetime import datetime

class Game(db.Model):
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    difficulty = db.Column(db.String(50), default='medium')
    cover_image = db.Column(db.String(10), default='🎮')  # Emoji icon
    platform = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default='backlog')  # playing, completed, backlog
    progress_percentage = db.Column(db.Integer, default=0)
    hours_played = db.Column(db.Float, default=0.0)
    last_played = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to user is defined in User model via backref='user'
    # This creates a 'user' attribute on Game automatically
    
    # Quest relationship is defined in Quest model with backref='quests'
    
    def __repr__(self):
        return f'<Game {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'genre': self.genre,
            'difficulty': self.difficulty,
            'cover_image': self.cover_image,
            'platform': self.platform,
            'status': self.status,
            'progress_percentage': self.progress_percentage,
            'hours_played': self.hours_played,
            'last_played': self.last_played.isoformat() if self.last_played else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }