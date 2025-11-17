# websocket/events.py
from flask_socketio import emit, join_room, leave_room
from flask_jwt_extended import decode_token
from models.game import Game
from utils.database import db

connected_users = {}

def register_socketio_events(socketio):
    """Register all WebSocket event handlers"""
    
    @socketio.on('connect')
    def handle_connect(auth):
        """Handle client connection"""
        try:
            token = auth.get('token')
            if token:
                decoded = decode_token(token)
                user_id = decoded['sub']
                connected_users[request.sid] = {
                    'user_id': user_id,
                    'socket_id': request.sid
                }
                join_room(f'user:{user_id}')
                emit('connected', {
                    'message': 'Connected to GrimoreGame server',
                    'user_id': user_id
                })
                print(f'✅ User {user_id} connected')
        except Exception as e:
            print(f'❌ Connection error: {e}')
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        if request.sid in connected_users:
            user_info = connected_users[request.sid]
            print(f'❌ User {user_info["user_id"]} disconnected')
            del connected_users[request.sid]
    
    @socketio.on('game:start')
    def handle_game_start(data):
        """Handle game session start"""
        try:
            game_id = data.get('gameId')
            join_room(f'game:{game_id}')
            emit('game:started', {'gameId': game_id})
            print(f'🎮 Game {game_id} session started')
        except Exception as e:
            emit('error', {'message': str(e)})
    
    @socketio.on('game:end')
    def handle_game_end(data):
        """Handle game session end"""
        try:
            game_id = data.get('gameId')
            leave_room(f'game:{game_id}')
            emit('game:ended', {'gameId': game_id})
            print(f'🛑 Game {game_id} session ended')
        except Exception as e:
            emit('error', {'message': str(e)})
    
    @socketio.on('progress:update')
    def handle_progress_update(data):
        """Handle progress update"""
        try:
            game_id = data.get('gameId')
            progress = data.get('progress')
            playtime = data.get('playtime')
            
            # Update in database
            game = Game.query.get(game_id)
            if game:
                game.progress = progress
                game.playtime = playtime
                db.session.commit()
            
            # Broadcast to user's rooms
            user_info = connected_users.get(request.sid)
            if user_info:
                socketio.emit('progress:updated', data, room=f'user:{user_info["user_id"]}')
            
            print(f'📊 Progress updated for game {game_id}: {progress}%')
        except Exception as e:
            emit('error', {'message': str(e)})
    
    @socketio.on('ai:analyze')
    def handle_ai_analyze(data):
        """Handle AI analysis request"""
        try:
            game_id = data.get('gameId')
            screenshot = data.get('screenshot')
            
            emit('ai:analyzing', {'status': 'processing'})
            
            # TODO: Integrate actual AI analysis here
            # For now, return mock data
            socketio.emit('ai:result', {
                'detectedObjects': [],
                'detectedText': [],
                'suggestedActions': []
            })
            
            print(f'🔍 AI analysis requested for game {game_id}')
        except Exception as e:
            emit('error', {'message': str(e)})
    
    @socketio.on('hint:request')
    def handle_hint_request(data):
        """Handle hint request"""
        try:
            quest_id = data.get('questId')
            context = data.get('context')
            
            emit('hint:generating', {'questId': quest_id})
            
            # TODO: Integrate actual AI hint generation
            socketio.emit('hint:generated', {
                'questId': quest_id,
                'hint': 'AI-generated hint would appear here'
            })
            
            print(f'💡 Hint requested for quest {quest_id}')
        except Exception as e:
            emit('error', {'message': str(e)})
    
    @socketio.on('sync:request')
    def handle_sync_request():
        """Handle sync request"""
        try:
            user_info = connected_users.get(request.sid)
            if user_info:
                user_id = user_info['user_id']
                games = Game.query.filter_by(user_id=user_id).order_by(Game.updated_at.desc()).limit(10).all()
                
                emit('sync:data', {
                    'games': [game.to_dict() for game in games],
                    'timestamp': datetime.utcnow().isoformat()
                })
                
                print(f'🔄 Sync completed for user {user_id}')
        except Exception as e:
            emit('error', {'message': str(e)})

from datetime import datetime
from flask import request