# routes/hints.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.game import Game
from models.quest import Quest
from models.hint import Hint
from utils.database import db

hints_bp = Blueprint('hints', __name__)

@hints_bp.route('/quest/<int:quest_id>', methods=['GET'])
@jwt_required()
def get_hints(quest_id):
    """Get all hints for a quest"""
    try:
        user_id = get_jwt_identity()
        quest = Quest.query.join(Game).filter(
            Quest.id == quest_id,
            Game.user_id == user_id
        ).first()
        
        if not quest:
            return jsonify({'error': 'Quest not found'}), 404
        
        hints = Hint.query.filter_by(quest_id=quest_id).order_by(Hint.created_at.asc()).all()
        
        return jsonify({'hints': [hint.to_dict() for hint in hints]}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@hints_bp.route('/', methods=['POST'])
@jwt_required()
def create_hint():
    """Create new hint"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not all(k in data for k in ['quest_id', 'hint_text']):
            return jsonify({'error': 'Quest ID and hint text required'}), 400
        
        # Verify quest belongs to user
        quest = Quest.query.join(Game).filter(
            Quest.id == data['quest_id'],
            Game.user_id == user_id
        ).first()
        
        if not quest:
            return jsonify({'error': 'Quest not found'}), 404
        
        hint = Hint(
            quest_id=data['quest_id'],
            hint_text=data['hint_text'],
            hint_type=data.get('hint_type', 'general')
        )
        
        db.session.add(hint)
        
        # Update quest hints counter
        quest.hints_used += 1
        
        db.session.commit()
        
        return jsonify({'hint': hint.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@hints_bp.route('/<int:hint_id>', methods=['GET'])
@jwt_required()
def get_hint(hint_id):
    """Get specific hint"""
    try:
        user_id = get_jwt_identity()
        hint = Hint.query.join(Quest).join(Game).filter(
            Hint.id == hint_id,
            Game.user_id == user_id
        ).first()
        
        if not hint:
            return jsonify({'error': 'Hint not found'}), 404
        
        # Increment frequency
        hint.frequency_shown += 1
        db.session.commit()
        
        return jsonify({'hint': hint.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@hints_bp.route('/<int:hint_id>/rate', methods=['POST'])
@jwt_required()
def rate_hint(hint_id):
    """Rate hint helpfulness"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if 'rating' not in data or not (1 <= data['rating'] <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        hint = Hint.query.join(Quest).join(Game).filter(
            Hint.id == hint_id,
            Game.user_id == user_id
        ).first()
        
        if not hint:
            return jsonify({'error': 'Hint not found'}), 404
        
        hint.helpfulness_rating = data['rating']
        db.session.commit()
        
        return jsonify({'hint': hint.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@hints_bp.route('/<int:hint_id>', methods=['DELETE'])
@jwt_required()
def delete_hint(hint_id):
    """Delete hint"""
    try:
        user_id = get_jwt_identity()
        hint = Hint.query.join(Quest).join(Game).filter(
            Hint.id == hint_id,
            Game.user_id == user_id
        ).first()
        
        if not hint:
            return jsonify({'error': 'Hint not found'}), 404
        
        quest = hint.quest
        db.session.delete(hint)
        quest.hints_used = max(0, quest.hints_used - 1)
        db.session.commit()
        
        return jsonify({'message': 'Hint deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@hints_bp.route('/game/<int:game_id>/stats', methods=['GET'])
@jwt_required()
def get_hint_stats(game_id):
    """Get hint statistics for a game"""
    try:
        user_id = get_jwt_identity()
        game = Game.query.filter_by(id=game_id, user_id=user_id).first()
        
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        
        hints = Hint.query.join(Quest).filter(Quest.game_id == game_id).all()
        
        stats = {
            'total_hints': len(hints),
            'general_hints': len([h for h in hints if h.hint_type == 'general']),
            'specific_hints': len([h for h in hints if h.hint_type == 'specific']),
            'solution_hints': len([h for h in hints if h.hint_type == 'solution']),
            'avg_rating': sum(h.helpfulness_rating for h in hints if h.helpfulness_rating) / len([h for h in hints if h.helpfulness_rating]) if any(h.helpfulness_rating for h in hints) else None
        }
        
        return jsonify({'stats': stats}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500