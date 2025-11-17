# routes/games.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.database import db
from models.game import Game
from models.user import User
from datetime import datetime

games_bp = Blueprint('games', __name__)

@games_bp.route('', methods=['GET'])
@jwt_required()
def get_games():
    """Get all games for the current user"""
    try:
        user_id = get_jwt_identity()
        games = Game.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'games': [{
                'id': g.id,
                'name': g.name,
                'description': g.description,
                'genre': g.genre,
                'difficulty': g.difficulty,
                'cover_image': g.cover_image,
                'platform': g.platform,
                'status': g.status,
                'progress_percentage': g.progress_percentage,
                'hours_played': g.hours_played,
                'last_played': g.last_played.isoformat() if g.last_played else None
            } for g in games]
        }), 200
    except Exception as e:
        print(f"Get games error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@games_bp.route('', methods=['POST'])
@jwt_required()
def create_game():
    """Create a new game"""
    try:
        user_id = get_jwt_identity()
        data = request.json
        
        # Validate required fields
        if not data.get('name'):
            return jsonify({'error': 'Game name is required'}), 400
        
        new_game = Game(
            user_id=user_id,
            name=data.get('name'),
            description=data.get('description', ''),
            genre=data.get('genre', 'Unknown'),
            difficulty=data.get('difficulty', 'medium'),
            cover_image=data.get('cover_image', '🎮'),
            platform=data.get('platform', 'PC'),
            status='backlog',
            progress_percentage=0,
            hours_played=0.0
        )
        
        db.session.add(new_game)
        db.session.commit()
        
        return jsonify({
            'message': 'Game added successfully',
            'game': {
                'id': new_game.id,
                'name': new_game.name,
                'genre': new_game.genre,
                'difficulty': new_game.difficulty,
                'cover_image': new_game.cover_image
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Create game error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@games_bp.route('/<int:game_id>', methods=['GET'])
@jwt_required()
def get_game(game_id):
    """Get a single game"""
    try:
        user_id = get_jwt_identity()
        game = Game.query.filter_by(id=game_id, user_id=user_id).first()
        
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        
        return jsonify({
            'game': {
                'id': game.id,
                'name': game.name,
                'description': game.description,
                'genre': game.genre,
                'difficulty': game.difficulty,
                'cover_image': game.cover_image,
                'platform': game.platform,
                'status': game.status,
                'progress_percentage': game.progress_percentage,
                'hours_played': game.hours_played,
                'last_played': game.last_played.isoformat() if game.last_played else None
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@games_bp.route('/<int:game_id>', methods=['PATCH'])
@jwt_required()
def update_game(game_id):
    """Update a game"""
    try:
        user_id = get_jwt_identity()
        game = Game.query.filter_by(id=game_id, user_id=user_id).first()
        
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        
        data = request.json
        
        if 'name' in data:
            game.name = data['name']
        if 'description' in data:
            game.description = data['description']
        if 'genre' in data:
            game.genre = data['genre']
        if 'difficulty' in data:
            game.difficulty = data['difficulty']
        if 'status' in data:
            game.status = data['status']
        if 'progress_percentage' in data:
            game.progress_percentage = data['progress_percentage']
        if 'hours_played' in data:
            game.hours_played = data['hours_played']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Game updated successfully',
            'game': game.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@games_bp.route('/<int:game_id>', methods=['DELETE'])
@jwt_required()
def delete_game(game_id):
    """Delete a game"""
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