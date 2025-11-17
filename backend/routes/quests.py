# routes/quests.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.database import db
from models.quest import Quest
from models.game import Game

quests_bp = Blueprint('quests', __name__)

@quests_bp.route('', methods=['POST'])
@jwt_required()
def create_quest():
    """Create a new quest"""
    try:
        data = request.json
        user_id = get_jwt_identity()
        
        # Validate required fields
        if not data.get('game_id'):
            return jsonify({'error': 'game_id is required'}), 400
        
        if not data.get('name') and not data.get('title'):
            return jsonify({'error': 'Quest name is required'}), 400
        
        # Check if game exists
        game = Game.query.get(data.get('game_id'))
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        
        # Create new quest
        new_quest = Quest(
            game_id=data.get('game_id'),
            name=data.get('name') or data.get('title'),
            description=data.get('description', ''),
            difficulty=data.get('difficulty', 5),
            status='active',
            completed=False
        )
        
        db.session.add(new_quest)
        db.session.commit()
        
        return jsonify({
            'message': 'Quest created successfully',
            'quest': {
                'id': new_quest.id,
                'name': new_quest.name,
                'description': new_quest.description,
                'difficulty': new_quest.difficulty,
                'status': new_quest.status,
                'completed': new_quest.completed,
                'game_id': new_quest.game_id
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@quests_bp.route('/game/<int:game_id>', methods=['GET'])
@jwt_required()
def get_game_quests(game_id):
    """Get all quests for a specific game"""
    try:
        user_id = get_jwt_identity()
        
        # Check if game exists
        game = Game.query.get(game_id)
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        
        # Get all quests for this game
        quests = Quest.query.filter_by(game_id=game_id).all()
        
        return jsonify({
            'quests': [{
                'id': q.id,
                'name': q.name,
                'description': q.description,
                'difficulty': q.difficulty,
                'status': q.status,
                'completed': q.completed,
                'game_id': q.game_id,
                'created_at': q.created_at.isoformat() if hasattr(q, 'created_at') and q.created_at else None
            } for q in quests]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quests_bp.route('/<int:quest_id>', methods=['GET'])
@jwt_required()
def get_quest(quest_id):
    """Get a single quest"""
    try:
        user_id = get_jwt_identity()
        quest = Quest.query.get_or_404(quest_id)
        
        return jsonify({
            'quest': {
                'id': quest.id,
                'name': quest.name,
                'description': quest.description,
                'difficulty': quest.difficulty,
                'status': quest.status,
                'completed': quest.completed,
                'game_id': quest.game_id
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@quests_bp.route('/<int:quest_id>', methods=['PATCH'])
@jwt_required()
def update_quest(quest_id):
    """Update a quest"""
    try:
        user_id = get_jwt_identity()
        quest = Quest.query.get_or_404(quest_id)
        data = request.json
        
        # Update fields if provided
        if 'name' in data:
            quest.name = data['name']
        if 'description' in data:
            quest.description = data['description']
        if 'difficulty' in data:
            quest.difficulty = data['difficulty']
        if 'status' in data:
            quest.status = data['status']
        if 'completed' in data:
            quest.completed = data['completed']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Quest updated successfully',
            'quest': {
                'id': quest.id,
                'name': quest.name,
                'description': quest.description,
                'difficulty': quest.difficulty,
                'status': quest.status,
                'completed': quest.completed
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@quests_bp.route('/<int:quest_id>', methods=['DELETE'])
@jwt_required()
def delete_quest(quest_id):
    """Delete a quest"""
    try:
        user_id = get_jwt_identity()
        quest = Quest.query.get_or_404(quest_id)
        
        db.session.delete(quest)
        db.session.commit()
        
        return jsonify({'message': 'Quest deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@quests_bp.route('/<int:quest_id>/complete', methods=['POST'])
@jwt_required()
def complete_quest(quest_id):
    """Mark a quest as complete"""
    try:
        user_id = get_jwt_identity()
        quest = Quest.query.get_or_404(quest_id)
        
        quest.completed = True
        quest.status = 'completed'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Quest completed! 🎉',
            'quest': {
                'id': quest.id,
                'name': quest.name,
                'completed': quest.completed,
                'status': quest.status
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@quests_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_quests():
    """Get all quests across all games for the current user"""
    try:
        user_id = get_jwt_identity()
        
        # Get all games for this user
        games = Game.query.filter_by(user_id=user_id).all()
        game_ids = [g.id for g in games]
        
        # Get all quests for these games
        quests = Quest.query.filter(Quest.game_id.in_(game_ids)).all()
        
        return jsonify({
            'quests': [{
                'id': q.id,
                'name': q.name,
                'description': q.description,
                'difficulty': q.difficulty,
                'status': q.status,
                'completed': q.completed,
                'game_id': q.game_id
            } for q in quests]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500