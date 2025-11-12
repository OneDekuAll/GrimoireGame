# app.py
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from config import Config
from utils.database import db, init_db
from routes.auth import auth_bp
from routes.games import games_bp
from routes.quests import quests_bp
from routes.hints import hints_bp
from websocket.events import register_socketio_events

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
CORS(app)
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(games_bp, url_prefix='/api/games')
app.register_blueprint(quests_bp, url_prefix='/api/quests')
app.register_blueprint(hints_bp, url_prefix='/api/hints')

# Register WebSocket events
register_socketio_events(socketio)

# Health check
@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'GrimoreGame Backend Running'}, 200

# Initialize database
with app.app_context():
    init_db()

if __name__ == '__main__':
    print('🚀 Starting GrimoreGame Backend Server...')
    print(f'📡 Server running on port {Config.PORT}')
    socketio.run(app, host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)