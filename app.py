from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Game data storage
quests = [
    {
        "id": 1,
        "title": "Defeat the Shadow Lord",
        "description": "A legendary quest to defeat the ancient evil.",
        "progress": 30,
        "active": True
    }
]

settings = {
    "hint_frequency": 50,
    "auto_hints": False,
    "smart_hints": True,
    "community_tips": True,
    "theme": "default"
}

# User's game library
game_library = [
    {
        "id": 1,
        "title": "Elder Scrolls V: Skyrim",
        "hours_played": 127,
        "last_played": "2025-10-12",
        "status": "playing",
        "cover": "🐉"
    },
    {
        "id": 2,
        "title": "The Witcher 3",
        "hours_played": 89,
        "last_played": "2025-10-10",
        "status": "playing",
        "cover": "🗡️"
    }
]

# Color themes - EXPANDED
themes = {
    "default": {
        "name": "Mystic Gold",
        "primary": "#d4af37",
        "secondary": "#b8860b",
        "accent": "#90ee90",
        "danger": "#dc143c",
        "bg_primary": "rgba(26, 15, 62, 0.98)",
        "bg_secondary": "rgba(15, 10, 46, 0.98)"
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
    "galaxy": {
        "name": "Galaxy Purple",
        "primary": "#a020f0",
        "secondary": "#7b2cbf",
        "accent": "#c77dff",
        "danger": "#dc143c",
        "bg_primary": "rgba(40, 10, 62, 0.98)",
        "bg_secondary": "rgba(30, 5, 46, 0.98)"
    }
}

adventures = [
    {"name": "Elder Scrolls: Mystic Realms", "difficulty": "Master", "description": "Ancient prophecies await"},
    {"name": "Witcher's Quest", "difficulty": "Expert", "description": "Hunt monsters in dark forests"},
    {"name": "Crystal Defenders", "difficulty": "Novice", "description": "Protect the sacred crystals"},
    {"name": "Guardian's Shield", "difficulty": "Adept", "description": "Defend the realm from darkness"}
]

@app.route('/')
def home():
    current_theme = themes.get(settings['theme'], themes['default'])
    return render_template('home.html', adventures=adventures, theme=current_theme)

@app.route('/library')
def library():
    current_theme = themes.get(settings['theme'], themes['default'])
    return render_template('library.html', games=game_library, theme=current_theme)

@app.route('/quest-grimoire')
def quest_grimoire():
    current_theme = themes.get(settings['theme'], themes['default'])
    return render_template('quest_grimoire.html', quests=quests, theme=current_theme)

@app.route('/settings')
def settings_page():
    current_theme = themes.get(settings['theme'], themes['default'])
    return render_template('settings.html', settings=settings, themes=themes, theme=current_theme)

@app.route('/game/<game_name>')
def game_play(game_name):
    current_theme = themes.get(settings['theme'], themes['default'])
    return render_template('game_play.html', game_name=game_name, theme=current_theme)

@app.route('/fallback')
def fallback():
    current_theme = themes.get(settings['theme'], themes['default'])
    return render_template('fallback.html', theme=current_theme)

# API endpoints
@app.route('/api/library', methods=['GET', 'POST'])
def api_library():
    if request.method == 'POST':
        data = request.json
        game = {
            "id": len(game_library) + 1,
            "title": data.get('title'),
            "hours_played": 0,
            "last_played": datetime.now().strftime("%Y-%m-%d"),
            "status": "backlog",
            "cover": data.get('cover', '🎮')
        }
        game_library.append(game)
        return jsonify(game), 201
    return jsonify(game_library)

@app.route('/api/library/<int:game_id>', methods=['PUT', 'DELETE'])
def api_library_detail(game_id):
    game = next((g for g in game_library if g['id'] == game_id), None)
    
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    if request.method == 'PUT':
        data = request.json
        game.update(data)
        return jsonify(game)
    
    if request.method == 'DELETE':
        game_library.remove(game)
        return jsonify({"message": "Game removed"}), 200

@app.route('/api/quests', methods=['GET', 'POST'])
def api_quests():
    if request.method == 'POST':
        data = request.json
        quest = {
            "id": len(quests) + 1,
            "title": data.get('title'),
            "description": data.get('description'),
            "progress": 0,
            "active": False
        }
        quests.append(quest)
        return jsonify(quest), 201
    return jsonify(quests)

@app.route('/api/quests/<int:quest_id>', methods=['PUT', 'DELETE'])
def api_quest_detail(quest_id):
    quest = next((q for q in quests if q['id'] == quest_id), None)
    
    if not quest:
        return jsonify({"error": "Quest not found"}), 404
    
    if request.method == 'PUT':
        data = request.json
        quest.update(data)
        return jsonify(quest)
    
    if request.method == 'DELETE':
        quests.remove(quest)
        return jsonify({"message": "Quest deleted"}), 200

@app.route('/api/settings', methods=['GET', 'POST'])
def api_settings():
    global settings
    if request.method == 'POST':
        settings.update(request.json)
        return jsonify(settings)
    return jsonify(settings)

if __name__ == '__main__':
    app.run(debug=True)