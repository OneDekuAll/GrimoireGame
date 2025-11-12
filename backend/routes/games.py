# routes/games.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.game import Game
from models.quest import Quest
from utils.database import db
from datetime import datetime

games_bp = Blueprint('games', __name__)

@games_bp.route('/', methods=['GET'])
@jwt_required()
def get_games():
    """Get all games for current user"""
    try:
        user_id = get_jwt_identity()
        games = Game.query.filter_by(user_id=user_id).order_by(Game.updated_at.desc()).all()
        
        games_data = []
        for game in games:
            game_dict = game.to_dict()
            total_quests = Quest.query.filter_by(game_id=game.id).count()
            completed_quests = Quest.query.filter_by(game_id=game.id, status='completed').count()
            game_dict['total_quests'] = total_quests
            game_dict['completed_quests'] = completed_quests
            games_data.append(game_dict)
        
        return jsonify({'games': games_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@games_bp.route('/<int:game_id>', methods=['GET'])
@jwt_required()
def get_game(game_id):
    """Get single game"""
    try:
        user_id = get_jwt_identity()
        game = Game.query.filter_by(id=game_id, user_id=user_id).first()
        
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        
        game_dict = game.to_dict()
        total_quests = Quest.query.filter_by(game_id=game.id).count()
        completed_quests = Quest.query.filter_by(game_id=game.id, status='completed').count()
        game_dict['total_quests'] = total_quests
        game_dict['completed_quests'] = completed_quests
        
        return jsonify({'game': game_dict}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@games_bp.route('/', methods=['POST'])
@jwt_required()
def create_game():
    """Create new game"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not all(k in data for k in ['name', 'difficulty']):
            return jsonify({'error': 'Name and difficulty required'}), 400
        
        game = Game(
            user_id=user_id,
            name=data['name'],
            difficulty=data['difficulty'],
            genre=data.get('genre', 'Unknown'),
            cover_image=data.get('cover_image')
        )
        
        db.session.add(game)
        db.session.commit()
        
        return jsonify({'game': game.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@games_bp.route('/<int:game_id>', methods=['PATCH'])
@jwt_required()
def update_game(game_id):
    """Update game"""
    try:
        user_id = get_jwt_identity()
        game = Game.query.filter_by(id=game_id, user_id=user_id).first()
        
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        
        data = request.get_json()
        
        if 'progress' in data:
            game.progress = data['progress']
        if 'playtime' in data:
            game.playtime = data['playtime']
        if 'status' in data:
            game.status = data['status']
            if data['status'] == 'completed':
                game.completed_at = datetime.utcnow()
        if 'difficulty' in data:
            game.difficulty = data['difficulty']
        if 'genre' in data:
            game.genre = data['genre']
        if 'cover_image' in data:
            game.cover_image = data['cover_image']
        
        game.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'game': game.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@games_bp.route('/<int:game_id>', methods=['DELETE'])
@jwt_required()
def delete_game(game_id):
    """Delete game"""
    try:
        user_id = get_jwt_identity()
        game = Game.query.filter_by(id=game_id, user_id=user_id).first()
        
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        
        db.session.delete(game)
        db.session.commit()
        
        return jsonify({'message': 'Game deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@games_bp.route('/<int:game_id>/stats', methods=['GET'])
@jwt_required()
def get_game_stats(game_id):
    """Get game statistics"""
    try:
        user_id = get_jwt_identity()
        game = Game.query.filter_by(id=game_id, user_id=user_id).first()
        
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        
        total_quests = Quest.query.filter_by(game_id=game.id).count()
        completed_quests = Quest.query.filter_by(game_id=game.id, status='completed').count()
        
        stats = {
            'playtime': game.playtime,
            'progress': game.progress,
            'total_quests': total_quests,
            'completed_quests': completed_quests
        }
        
        return jsonify({'stats': stats}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500