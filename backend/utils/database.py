# utils/database.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    """Initialize database tables"""
    db.create_all()
    print('✅ Database initialized')