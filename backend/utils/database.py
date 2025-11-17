# utils/database.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    """Initialize the database and create all tables"""
    # Import all models here to ensure they're registered
    from models.user import User
    from models.game import Game
    from models.quest import Quest
    
    # Create all tables
    db.create_all()
    print('✅ Database tables created successfully!')