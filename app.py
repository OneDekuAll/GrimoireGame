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
    "community_tips": True
}

adventures = [
    {"name": "Elder Scrolls: Mystic Realms", "difficulty": "Master", "description": "Ancient prophecies await"},
    {"name": "Witcher's Quest", "difficulty": "Expert", "description": "Hunt monsters in dark forests"},
    {"name": "Crystal Defenders", "difficulty": "Novice", "description": "Protect the sacred crystals"},
    {"name": "Guardian's Shield", "difficulty": "Adept", "description": "Defend the realm from darkness"}
]

@app.route('/')
def home():
    return render_template('home.html', adventures=adventures)

@app.route('/quest-grimoire')
def quest_grimoire():
    return render_template('quest_grimoire.html', quests=quests)

@app.route('/settings')
def settings_page():
    return render_template('settings.html', settings=settings)

@app.route('/game/<game_name>')
def game_play(game_name):
    return render_template('game_play.html', game_name=game_name)

@app.route('/fallback')
def fallback():
    return render_template('fallback.html')

# API endpoints
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