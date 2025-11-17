# models/hint.py
from utils.database import db
from datetime import datetime

class Hint(db.Model):
    __tablename__ = 'hints'
    
    id = db.Column(db.Integer, primary_key=True)
    quest_id = db.Column(db.Integer, db.ForeignKey('quests.id'), nullable=False)
    hint_text = db.Column(db.Text, nullable=False)
    hint_type = db.Column(db.String(20), default='general')
    frequency_shown = db.Column(db.Integer, default=1)
    helpfulness_rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'quest_id': self.quest_id,
            'hint_text': self.hint_text,
            'hint_type': self.hint_type,
            'frequency_shown': self.frequency_shown,
            'helpfulness_rating': self.helpfulness_rating,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }