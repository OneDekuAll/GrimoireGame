# app.py
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from config import Config
from utils.database import db, init_db
from routes.auth import auth_bp
from routes.games import games_bp
from routes.quests import quests_bp
from routes.hints import hints_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
CORS(app)
db.init_app(app)
jwt = JWTManager(app)

# Use threading mode (works with Python 3.13)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(games_bp, url_prefix='/api/games')
app.register_blueprint(quests_bp, url_prefix='/api/quests')
app.register_blueprint(hints_bp, url_prefix='/api/hints')

@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'GrimoreGame Backend Running'}, 200

# Initialize database
with app.app_context():
    init_db()

if __name__ == '__main__':
    print('🚀 Starting GrimoreGame Backend Server...')
    print(f'📡 Server running on port {Config.PORT}')
    print(f'🔧 Using threading mode')
    socketio.run(app, host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)