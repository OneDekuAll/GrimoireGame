# routes/quests.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.game import Game
from models.quest import Quest
from models.hint import Hint
from utils.database import db
from datetime import datetime

quests_bp = Blueprint('quests', __name__)

@quests_bp.route('/game/<int:game_id>', methods=['GET'])
@jwt_required()
def get_quests(game_id):
    """Get all quests for a game"""
    try:
        user_id = get_jwt_identity()
        game = Game.query.filter_by(id=game_id, user_id=user_id).first()
        
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        
        quests = Quest.query.filter_by(game_id=game_id).order_by(Quest.created_at.desc()).all()
        
        quests_data = []
        for quest in quests:
            quest_dict = quest.to_dict()
            total_hints = Hint.query.filter_by(quest_id=quest.id).count()
            quest_dict['total_hints'] = total_hints
            quests_data.append(quest_dict)
        
        return jsonify({'quests': quests_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quests_bp.route('/<int:quest_id>', methods=['GET'])
@jwt_required()
def get_quest(quest_id):
    """Get single quest"""
    try:
        user_id = get_jwt_identity()
        quest = Quest.query.join(Game).filter(
            Quest.id == quest_id,
            Game.user_id == user_id
        ).first()
        
        if not quest:
            return jsonify({'error': 'Quest not found'}), 404
        
        quest_dict = quest.to_dict()
        total_hints = Hint.query.filter_by(quest_id=quest.id).count()
        quest_dict['total_hints'] = total_hints
        
        return jsonify({'quest': quest_dict}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quests_bp.route('/', methods=['POST'])
@jwt_required()
def create_quest():
    """Create new quest"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not all(k in data for k in ['game_id', 'name']):
            return jsonify({'error': 'Game ID and name required'}), 400
        
        # Verify game belongs to user
        game = Game.query.filter_by(id=data['game_id'], user_id=user_id).first()
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        
        quest = Quest(
            game_id=data['game_id'],
            name=data['name'],
            description=data.get('description', ''),
            difficulty=data.get('difficulty', 5)
        )
        
        db.session.add(quest)
        db.session.commit()
        
        return jsonify({'quest': quest.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@quests_bp.route('/<int:quest_id>', methods=['PATCH'])
@jwt_required()
def update_quest(quest_id):
    """Update quest"""
    try:
        user_id = get_jwt_identity()
        quest = Quest.query.join(Game).filter(
            Quest.id == quest_id,
            Game.user_id == user_id
        ).first()
        
        if not quest:
            return jsonify({'error': 'Quest not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            quest.name = data['name']
        if 'description' in data:
            quest.description = data['description']
        if 'status' in data:
            quest.status = data['status']
        if 'difficulty' in data:
            quest.difficulty = data['difficulty']
        if 'notes' in data:
            quest.notes = data['notes']
        if 'completion_time' in data:
            quest.completion_time = data['completion_time']
        
        quest.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'quest': quest.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@quests_bp.route('/<int:quest_id>', methods=['DELETE'])
@jwt_required()
def delete_quest(quest_id):
    """Delete quest"""
    try:
        user_id = get_jwt_identity()
        quest = Quest.query.join(Game).filter(
            Quest.id == quest_id,
            Game.user_id == user_id
        ).first()
        
        if not quest:
            return jsonify({'error': 'Quest not found'}), 404
        
        db.session.delete(quest)
        db.session.commit()
        
        return jsonify({'message': 'Quest deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@quests_bp.route('/<int:quest_id>/start', methods=['POST'])
@jwt_required()
def start_quest(quest_id):
    """Mark quest as started"""
    try:
        user_id = get_jwt_identity()
        quest = Quest.query.join(Game).filter(
            Quest.id == quest_id,
            Game.user_id == user_id
        ).first()
        
        if not quest:
            return jsonify({'error': 'Quest not found'}), 404
        
        quest.status = 'in_progress'
        quest.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'quest': quest.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@quests_bp.route('/<int:quest_id>/complete', methods=['POST'])
@jwt_required()
def complete_quest(quest_id):
    """Mark quest as completed"""
    try:
        user_id = get_jwt_identity()
        quest = Quest.query.join(Game).filter(
            Quest.id == quest_id,
            Game.user_id == user_id
        ).first()
        
        if not quest:
            return jsonify({'error': 'Quest not found'}), 404
        
        data = request.get_json() or {}
        
        quest.status = 'completed'
        quest.completion_time = data.get('completion_time')
        quest.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'quest': quest.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500