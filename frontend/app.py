from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from datetime import datetime
import requests
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Backend API URL
BACKEND_URL = 'http://localhost:5000/api'

# Themes (keeping your existing themes)
themes = {
    "default": {
         "name": "Galaxy Purple",
        "primary": "#a020f0",
        "secondary": "#7b2cbf",
        "accent": "#c77dff",
        "danger": "#dc143c",
        "bg_primary": "rgba(40, 10, 62, 0.98)",
        "bg_secondary": "rgba(30, 5, 46, 0.98)"
    },
    "gold": {
        "name": "Mystic Gold",
        "primary": "#d4af37",
        "secondary": "#b8860b",
        "accent": "#90ee90",
        "danger": "#dc143c",
        "bg_primary": "rgba(26, 15, 62, 0.98)",
        "bg_secondary": "rgba(15, 10, 46, 0.98)"
    },
    "cosmic": {
        "name": "Cosmic Void",
        "primary": "#8a2be2",
        "secondary": "#4b0082",
        "accent": "#da70d6",
        "danger": "#ff1493",
        "bg_primary": "rgba(20, 10, 40, 0.98)",
        "bg_secondary": "rgba(10, 5, 25, 0.98)"
    },
    "nebula": {
        "name": "Nebula Storm",
        "primary": "#ff00ff",
        "secondary": "#8b00ff",
        "accent": "#ff69b4",
        "danger": "#dc143c",
        "bg_primary": "rgba(50, 10, 50, 0.98)",
        "bg_secondary": "rgba(35, 5, 35, 0.98)"
    },
    "starlight": {
        "name": "Starlight Blue",
        "primary": "#00bfff",
        "secondary": "#1e90ff",
        "accent": "#87cefa",
        "danger": "#dc143c",
        "bg_primary": "rgba(10, 25, 50, 0.98)",
        "bg_secondary": "rgba(5, 15, 35, 0.98)"
    },
    "aurora": {
        "name": "Aurora Borealis",
        "primary": "#00ff7f",
        "secondary": "#00ced1",
        "accent": "#7fffd4",
        "danger": "#dc143c",
        "bg_primary": "rgba(10, 40, 50, 0.98)",
        "bg_secondary": "rgba(5, 25, 35, 0.98)"
    },
    "supernova": {
        "name": "Supernova Burst",
        "primary": "#ff4500",
        "secondary": "#ff8c00",
        "accent": "#ffd700",
        "danger": "#ff0000",
        "bg_primary": "rgba(50, 20, 10, 0.98)",
        "bg_secondary": "rgba(35, 10, 5, 0.98)"
    },
    "blackhole": {
        "name": "Black Hole",
        "primary": "#4169e1",
        "secondary": "#191970",
        "accent": "#6495ed",
        "danger": "#dc143c",
        "bg_primary": "rgba(5, 5, 15, 0.98)",
        "bg_secondary": "rgba(2, 2, 8, 0.98)"
    },
    "stardust": {
        "name": "Stardust Trail",
        "primary": "#ffd700",
        "secondary": "#daa520",
        "accent": "#fffacd",
        "danger": "#dc143c",
        "bg_primary": "rgba(40, 35, 50, 0.98)",
        "bg_secondary": "rgba(25, 20, 35, 0.98)"
    },
    "deepspace": {
        "name": "Deep Space",
        "primary": "#483d8b",
        "secondary": "#2f4f4f",
        "accent": "#6a5acd",
        "danger": "#dc143c",
        "bg_primary": "rgba(15, 10, 30, 0.98)",
        "bg_secondary": "rgba(8, 5, 18, 0.98)"
    },
    "emerald": {
        "name": "Emerald Forest",
        "primary": "#50c878",
        "secondary": "#2d5016",
        "accent": "#98fb98",
        "danger": "#dc143c",
        "bg_primary": "rgba(15, 46, 26, 0.98)",
        "bg_secondary": "rgba(10, 30, 15, 0.98)"
    },
    "crimson": {
        "name": "Crimson Blood",
        "primary": "#dc143c",
        "secondary": "#8b0000",
        "accent": "#ff6b6b",
        "danger": "#8b0000",
        "bg_primary": "rgba(62, 15, 26, 0.98)",
        "bg_secondary": "rgba(46, 10, 15, 0.98)"
    },
    "azure": {
        "name": "Azure Sky",
        "primary": "#4a9eff",
        "secondary": "#1e3a8a",
        "accent": "#87ceeb",
        "danger": "#dc143c",
        "bg_primary": "rgba(15, 26, 62, 0.98)",
        "bg_secondary": "rgba(10, 15, 46, 0.98)"
    },
    "amethyst": {
        "name": "Amethyst Dream",
        "primary": "#9966cc",
        "secondary": "#6a0dad",
        "accent": "#da70d6",
        "danger": "#dc143c",
        "bg_primary": "rgba(46, 15, 62, 0.98)",
        "bg_secondary": "rgba(30, 10, 46, 0.98)"
    },
    "silver": {
        "name": "Silver Moon",
        "primary": "#c0c0c0",
        "secondary": "#808080",
        "accent": "#e8e8e8",
        "danger": "#dc143c",
        "bg_primary": "rgba(40, 40, 50, 0.98)",
        "bg_secondary": "rgba(25, 25, 35, 0.98)"
    },
    "copper": {
        "name": "Copper Forge",
        "primary": "#b87333",
        "secondary": "#8b4513",
        "accent": "#cd853f",
        "danger": "#dc143c",
        "bg_primary": "rgba(50, 30, 20, 0.98)",
        "bg_secondary": "rgba(35, 20, 10, 0.98)"
    },
    "jade": {
        "name": "Jade Palace",
        "primary": "#00a86b",
        "secondary": "#006b3f",
        "accent": "#7fffd4",
        "danger": "#dc143c",
        "bg_primary": "rgba(15, 46, 40, 0.98)",
        "bg_secondary": "rgba(10, 30, 25, 0.98)"
    },
    "rose": {
        "name": "Rose Garden",
        "primary": "#ff69b4",
        "secondary": "#c71585",
        "accent": "#ffb6c1",
        "danger": "#dc143c",
        "bg_primary": "rgba(62, 15, 46, 0.98)",
        "bg_secondary": "rgba(46, 10, 30, 0.98)"
    },
    "amber": {
        "name": "Amber Sunset",
        "primary": "#ffbf00",
        "secondary": "#ff8c00",
        "accent": "#ffd700",
        "danger": "#dc143c",
        "bg_primary": "rgba(62, 40, 15, 0.98)",
        "bg_secondary": "rgba(46, 25, 10, 0.98)"
    },
    "sapphire": {
        "name": "Sapphire Ocean",
        "primary": "#0f52ba",
        "secondary": "#082567",
        "accent": "#6495ed",
        "danger": "#dc143c",
        "bg_primary": "rgba(15, 30, 62, 0.98)",
        "bg_secondary": "rgba(10, 20, 46, 0.98)"
    },
    "obsidian": {
        "name": "Obsidian Night",
        "primary": "#4a4a4a",
        "secondary": "#2a2a2a",
        "accent": "#6a6a6a",
        "danger": "#dc143c",
        "bg_primary": "rgba(20, 20, 25, 0.98)",
        "bg_secondary": "rgba(10, 10, 15, 0.98)"
    },
    "ruby": {
        "name": "Ruby Fire",
        "primary": "#e0115f",
        "secondary": "#9b111e",
        "accent": "#ff1493",
        "danger": "#8b0000",
        "bg_primary": "rgba(62, 10, 30, 0.98)",
        "bg_secondary": "rgba(46, 5, 20, 0.98)"
    },
    "turquoise": {
        "name": "Turquoise Wave",
        "primary": "#40e0d0",
        "secondary": "#00ced1",
        "accent": "#afeeee",
        "danger": "#dc143c",
        "bg_primary": "rgba(15, 46, 50, 0.98)",
        "bg_secondary": "rgba(10, 30, 35, 0.98)"
    },
    "lavender": {
        "name": "Lavender Fields",
        "primary": "#b57edc",
        "secondary": "#8b5a9e",
        "accent": "#dda0dd",
        "danger": "#dc143c",
        "bg_primary": "rgba(40, 25, 50, 0.98)",
        "bg_secondary": "rgba(25, 15, 35, 0.98)"
    },
    "coral": {
        "name": "Coral Reef",
        "primary": "#ff7f50",
        "secondary": "#ff6347",
        "accent": "#ffa07a",
        "danger": "#dc143c",
        "bg_primary": "rgba(62, 30, 25, 0.98)",
        "bg_secondary": "rgba(46, 20, 15, 0.98)"
    },
    "mint": {
        "name": "Mint Breeze",
        "primary": "#98ff98",
        "secondary": "#3eb489",
        "accent": "#aaffc3",
        "danger": "#dc143c",
        "bg_primary": "rgba(20, 46, 35, 0.98)",
        "bg_secondary": "rgba(15, 30, 25, 0.98)"
    },
    "sunset": {
        "name": "Sunset Horizon",
        "primary": "#ff6b35",
        "secondary": "#f7931e",
        "accent": "#ffb347",
        "danger": "#dc143c",
        "bg_primary": "rgba(62, 25, 15, 0.98)",
        "bg_secondary": "rgba(46, 15, 10, 0.98)"
    },
    "midnight": {
        "name": "Midnight Blue",
        "primary": "#191970",
        "secondary": "#000080",
        "accent": "#4169e1",
        "danger": "#dc143c",
        "bg_primary": "rgba(10, 10, 46, 0.98)",
        "bg_secondary": "rgba(5, 5, 30, 0.98)"
    },
    "volcanic": {
        "name": "Volcanic Ash",
        "primary": "#ff6347",
        "secondary": "#8b0000",
        "accent": "#ff4500",
        "danger": "#b22222",
        "bg_primary": "rgba(50, 15, 10, 0.98)",
        "bg_secondary": "rgba(35, 8, 5, 0.98)"
    },
    "arctic": {
        "name": "Arctic Ice",
        "primary": "#b0e0e6",
        "secondary": "#4682b4",
        "accent": "#e0ffff",
        "danger": "#dc143c",
        "bg_primary": "rgba(20, 30, 40, 0.98)",
        "bg_secondary": "rgba(10, 20, 30, 0.98)"
    },
    "toxicgreen": {
        "name": "Toxic Glow",
        "primary": "#39ff14",
        "secondary": "#00ff00",
        "accent": "#7fff00",
        "danger": "#dc143c",
        "bg_primary": "rgba(10, 40, 10, 0.98)",
        "bg_secondary": "rgba(5, 25, 5, 0.98)"
    },
    "neon": {
        "name": "Neon Lights",
        "primary": "#ff10f0",
        "secondary": "#ff00ff",
        "accent": "#00ffff",
        "danger": "#ff0066",
        "bg_primary": "rgba(20, 10, 30, 0.98)",
        "bg_secondary": "rgba(10, 5, 20, 0.98)"
    },
    "cyberpunk": {
        "name": "Cyberpunk City",
        "primary": "#00ffff",
        "secondary": "#ff00ff",
        "accent": "#ffff00",
        "danger": "#ff0000",
        "bg_primary": "rgba(10, 10, 25, 0.98)",
        "bg_secondary": "rgba(5, 5, 15, 0.98)"
    },
    "solarsystem": {
        "name": "Solar System",
        "primary": "#ffa500",
        "secondary": "#ff8c00",
        "accent": "#ffff00",
        "danger": "#dc143c",
        "bg_primary": "rgba(30, 20, 10, 0.98)",
        "bg_secondary": "rgba(20, 10, 5, 0.98)"
    },
    "moonlight": {
        "name": "Moonlight Silver",
        "primary": "#e6e6fa",
        "secondary": "#9370db",
        "accent": "#f0e68c",
        "danger": "#dc143c",
        "bg_primary": "rgba(30, 25, 40, 0.98)",
        "bg_secondary": "rgba(20, 15, 30, 0.98)"
    },
    "comet": {
        "name": "Comet Trail",
        "primary": "#00ffff",
        "secondary": "#4169e1",
        "accent": "#87ceeb",
        "danger": "#dc143c",
        "bg_primary": "rgba(10, 20, 40, 0.98)",
        "bg_secondary": "rgba(5, 10, 25, 0.98)"
    },
    "plasma": {
        "name": "Plasma Energy",
        "primary": "#ff00ff",
        "secondary": "#ff1493",
        "accent": "#ee82ee",
        "danger": "#dc143c",
        "bg_primary": "rgba(40, 10, 40, 0.98)",
        "bg_secondary": "rgba(25, 5, 25, 0.98)"
    },
    "quantumrealm": {
        "name": "Quantum Realm",
        "primary": "#9d00ff",
        "secondary": "#6a0dad",
        "accent": "#bf00ff",
        "danger": "#dc143c",
        "bg_primary": "rgba(25, 5, 35, 0.98)",
        "bg_secondary": "rgba(15, 2, 25, 0.98)"
    },
    "voidwalker": {
        "name": "Voidwalker",
        "primary": "#8a2be2",
        "secondary": "#000000",
        "accent": "#9370db",
        "danger": "#dc143c",
        "bg_primary": "rgba(10, 5, 20, 0.98)",
        "bg_secondary": "rgba(5, 2, 10, 0.98)"
    },
    "celestial": {
        "name": "Celestial Light",
        "primary": "#fffacd",
        "secondary": "#ffd700",
        "accent": "#ffffe0",
        "danger": "#dc143c",
        "bg_primary": "rgba(40, 35, 50, 0.98)",
        "bg_secondary": "rgba(25, 20, 35, 0.98)"
    }
}

# Auth decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Helper function to make authenticated API calls
def api_call(endpoint, method='GET', data=None):
    """Make API call to backend with authentication"""
    headers = {}
    if 'token' in session:
        headers['Authorization'] = f"Bearer {session['token']}"
    
    url = f"{BACKEND_URL}{endpoint}"
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method == 'PATCH':
            response = requests.patch(url, json=data, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        
        if response.status_code in [200, 201]:
            return response.json(), None
        else:
            return None, response.json().get('error', 'Unknown error')
    except Exception as e:
        return None, str(e)

# ========== AUTH ROUTES ==========

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        identifier = data.get('email')  # This field now accepts username or email
        password = data.get('password')
        
        try:
            response = requests.post(f'{BACKEND_URL}/auth/login', 
                                    json={'email': identifier, 'password': password})
            
            if response.status_code == 200:
                result = response.json()
                session['token'] = result['token']
                session['user'] = result['user']
                
                if request.is_json:
                    return jsonify({'success': True, 'redirect': url_for('home')})
                return redirect(url_for('home'))
            else:
                error = response.json().get('error', 'Login failed')
                if request.is_json:
                    return jsonify({'success': False, 'error': error}), 400
                flash(error, 'danger')
        except Exception as e:
            if request.is_json:
                return jsonify({'success': False, 'error': str(e)}), 500
            flash(f'Error: {str(e)}', 'danger')
    
    current_theme = themes.get('default')
    return render_template('login.html', theme=current_theme)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        try:
            response = requests.post(f'{BACKEND_URL}/auth/register',
                                    json={'username': username, 'email': email, 'password': password})
            
            if response.status_code == 201:
                result = response.json()
                session['token'] = result['token']
                session['user'] = result['user']
                
                if request.is_json:
                    return jsonify({'success': True, 'redirect': url_for('home')})
                return redirect(url_for('home'))
            else:
                error = response.json().get('error', 'Registration failed')
                if request.is_json:
                    return jsonify({'success': False, 'error': error}), 400
                flash(error, 'danger')
        except Exception as e:
            if request.is_json:
                return jsonify({'success': False, 'error': str(e)}), 500
            flash(f'Error: {str(e)}', 'danger')
    
    current_theme = themes.get('default')
    return render_template('register.html', theme=current_theme)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

# ========== MAIN ROUTES ==========

@app.route('/')
@login_required
def home():
    current_theme = themes.get(session.get('theme', 'default'), themes['default'])
    
    # Get user's games from backend
    games_data, error = api_call('/games')
    games = games_data.get('games', []) if games_data else []
    
    # Mock adventures for now
    adventures = [
        {"name": "Elder Scrolls: Mystic Realms", "difficulty": "Master", "description": "Ancient prophecies await"},
        {"name": "Witcher's Quest", "difficulty": "Expert", "description": "Hunt monsters in dark forests"},
        {"name": "Crystal Defenders", "difficulty": "Novice", "description": "Protect the sacred crystals"},
        {"name": "Guardian's Shield", "difficulty": "Adept", "description": "Defend the realm from darkness"}
    ]
    
    return render_template('home.html', 
                         adventures=adventures, 
                         games=games, 
                         theme=current_theme,
                         user=session.get('user'))

@app.route('/library')
@login_required
def library():
    current_theme = themes.get(session.get('theme', 'default'), themes['default'])
    
    # Get games from backend
    games_data, error = api_call('/games')
    if error:
        flash(f'Error loading games: {error}', 'danger')
        games = []
    else:
        games = games_data.get('games', [])
    
    return render_template('library.html', 
                         games=games, 
                         theme=current_theme,
                         user=session.get('user'))

@app.route('/quest-grimoire')
@login_required
def quest_grimoire():
    current_theme = themes.get(session.get('theme', 'default'), themes['default'])
    
    # Get all quests from all games
    games_data, error = api_call('/games')
    quests = []
    
    if games_data and 'games' in games_data:
        for game in games_data['games']:
            quests_data, error = api_call(f'/quests/game/{game["id"]}')
            if quests_data and 'quests' in quests_data:
                for quest in quests_data['quests']:
                    quest['game_name'] = game['name']
                    quests.append(quest)
    
    return render_template('quest_grimoire.html', 
                         quests=quests, 
                         theme=current_theme,
                         user=session.get('user'))

@app.route('/game/<int:game_id>')
@login_required
def game_play(game_id):
    current_theme = themes.get(session.get('theme', 'default'), themes['default'])
    
    # Get game details from backend
    game_data, error = api_call(f'/games/{game_id}')
    if error:
        flash(f'Game not found: {error}', 'danger')
        return redirect(url_for('library'))
    
    game = game_data.get('game', {})
    
    # Get quests for this game
    quests_data, error = api_call(f'/quests/game/{game_id}')
    quests = quests_data.get('quests', []) if quests_data else []
    
    return render_template('game_play.html', 
                         game=game, 
                         quests=quests,
                         theme=current_theme,
                         user=session.get('user'))

@app.route('/settings')
@login_required
def settings_page():
    current_theme = themes.get(session.get('theme', 'default'), themes['default'])
    
    # Get user preferences from backend
    user_data = session.get('user', {})
    settings = user_data.get('preferences', {
        'hint_frequency': 50,
        'auto_hints': False,
        'smart_hints': True,
        'community_tips': True,
        'theme': 'default'
    })
    
    return render_template('settings.html', 
                         settings=settings, 
                         themes=themes, 
                         theme=current_theme,
                         user=session.get('user'))

@app.route('/fallback')
def fallback():
    current_theme = themes.get(session.get('theme', 'default'), themes['default'])
    return render_template('fallback.html', theme=current_theme)

# ========== API ENDPOINTS ==========

@app.route('/api/library', methods=['GET', 'POST'])
@login_required
def api_library():
    if request.method == 'POST':
        data = request.json
        game_data = {
            'name': data.get('title'),
            'difficulty': data.get('difficulty', 'medium'),
            'genre': data.get('genre', 'Unknown'),
            'cover_image': data.get('cover')
        }
        
        result, error = api_call('/games', method='POST', data=game_data)
        if error:
            return jsonify({"error": error}), 400
        return jsonify(result), 201
    
    # GET request
    result, error = api_call('/games')
    if error:
        return jsonify({"error": error}), 400
    return jsonify(result.get('games', []))

@app.route('/api/library/<int:game_id>', methods=['PUT', 'DELETE'])
@login_required
def api_library_detail(game_id):
    if request.method == 'PUT':
        data = request.json
        result, error = api_call(f'/games/{game_id}', method='PATCH', data=data)
        if error:
            return jsonify({"error": error}), 400
        return jsonify(result)
    
    if request.method == 'DELETE':
        result, error = api_call(f'/games/{game_id}', method='DELETE')
        if error:
            return jsonify({"error": error}), 400
        return jsonify({"message": "Game removed"}), 200

@app.route('/api/quests', methods=['GET', 'POST'])
@login_required
def api_quests():
    if request.method == 'POST':
        data = request.json
        quest_data = {
            'game_id': data.get('game_id'),
            'name': data.get('title'),
            'description': data.get('description'),
            'difficulty': data.get('difficulty', 5)
        }
        
        result, error = api_call('/quests', method='POST', data=quest_data)
        if error:
            return jsonify({"error": error}), 400
        return jsonify(result), 201
    
    # Get all quests from all games
    games_data, error = api_call('/games')
    all_quests = []
    
    if games_data and 'games' in games_data:
        for game in games_data['games']:
            quests_data, error = api_call(f'/quests/game/{game["id"]}')
            if quests_data and 'quests' in quests_data:
                all_quests.extend(quests_data['quests'])
    
    return jsonify(all_quests)

@app.route('/api/quests/<int:quest_id>', methods=['PUT', 'DELETE'])
@login_required
def api_quest_detail(quest_id):
    if request.method == 'PUT':
        data = request.json
        result, error = api_call(f'/quests/{quest_id}', method='PATCH', data=data)
        if error:
            return jsonify({"error": error}), 400
        return jsonify(result)
    
    if request.method == 'DELETE':
        result, error = api_call(f'/quests/{quest_id}', method='DELETE')
        if error:
            return jsonify({"error": error}), 400
        return jsonify({"message": "Quest deleted"}), 200

@app.route('/api/settings', methods=['GET', 'POST'])
@login_required
def api_settings():
    if request.method == 'POST':
        data = request.json
        # Update theme in session
        if 'theme' in data:
            session['theme'] = data['theme']
        
        # Update preferences in backend
        result, error = api_call('/auth/preferences', method='PATCH', data={'preferences': data})
        if error:
            return jsonify({"error": error}), 400
        
        # Update session user data
        if 'user' in session:
            session['user']['preferences'] = data
        
        return jsonify(data)
    
    # GET request
    user = session.get('user', {})
    return jsonify(user.get('preferences', {}))

if __name__ == '__main__':
    # Run frontend on port 3000
    app.run(debug=True, port=3000)