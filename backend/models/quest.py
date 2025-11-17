# models/quest.py
from utils.database import db
from datetime import datetime

class Quest(db.Model):
    __tablename__ = 'quests'
    
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.Integer, default=5)  # 1-10 scale
    status = db.Column(db.String(50), default='active')  # active, completed, failed
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to game
    game = db.relationship('Game', backref='quests')
    
    def __repr__(self):
        return f'<Quest {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'game_id': self.game_id,
            'name': self.name,
            'description': self.description,
            'difficulty': self.difficulty,
            'status': self.status,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }