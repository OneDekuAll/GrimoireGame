// src/components/views/HomeView.tsx
import React from 'react';
import { Screen, Game } from '../../types'; // Ensure 'Screen' is defined as a valid type in '../../types'
import { Settings, Shield, Sparkles } from 'lucide-react';

interface HomeViewProps {
  setCurrentView: (view: Screen) => void; // Ensure 'Screen' is defined in '../../types'
  userGames: Game[];
  setSelectedGame: (game: Game) => void;
}

export const HomeView: React.FC<HomeViewProps> = ({
  setCurrentView,
  userGames,
  setSelectedGame
}) => {
  const difficultyColors: Record<string, string> = {
    'Master': 'bg-gradient-to-br from-red-900 to-red-950 text-red-200 border-red-950',
    'Expert': 'bg-gradient-to-br from-orange-900 to-orange-950 text-orange-200 border-orange-950',
    'Adept': 'bg-gradient-to-br from-blue-900 to-blue-950 text-blue-200 border-blue-950',
    'Novice': 'bg-gradient-to-br from-green-900 to-green-950 text-green-200 border-green-950'
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-950 via-stone-950 to-stone-900 p-8 relative overflow-hidden">
      {/* Background texture */}
      <div className="absolute inset-0 opacity-5" style={{
        backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(139, 69, 19, 0.1) 2px, rgba(139, 69, 19, 0.1) 4px)'
      }}></div>

      {/* Main content */}
      <div className="max-w-6xl mx-auto relative">
        {/* Header */}
        <div className="bg-gradient-to-br from-amber-100 via-yellow-50 to-amber-100 rounded-lg shadow-2xl p-12 border-8 border-amber-900 relative">
          {/* Decorative corners */}
          <div className="absolute top-8 left-8 w-16 h-16 border-t-4 border-l-4 border-amber-900 opacity-30"></div>
          <div className="absolute top-8 right-8 w-16 h-16 border-t-4 border-r-4 border-amber-900 opacity-30"></div>
          <div className="absolute bottom-8 left-8 w-16 h-16 border-b-4 border-l-4 border-amber-900 opacity-30"></div>
          <div className="absolute bottom-8 right-8 w-16 h-16 border-b-4 border-r-4 border-amber-900 opacity-30"></div>

          {/* Title */}
          <div className="text-center space-y-4 mb-12">
            <div className="flex items-center justify-center gap-4 mb-6">
              <div className="w-16 h-0.5 bg-amber-900"></div>
              <div className="w-8 h-8 text-amber-800">✨</div>
              <h1 className="text-6xl font-serif text-amber-900 tracking-widest">GrimoireGame</h1>
              <Sparkles className="w-8 h-8 text-amber-800" />
              <div className="w-16 h-0.5 bg-amber-900"></div>
            </div>
            <p className="text-amber-800 text-xl italic">Thy Mystical Gaming Companion</p>
          </div>

          {/* Game library */}
          <div className="mb-8">
            <h2 className="text-4xl font-serif text-amber-900 text-center mb-8 relative">
              <span className="relative inline-block">
                Thy Sacred Library
                <div className="absolute -bottom-2 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-amber-900 to-transparent"></div>
              </span>
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {userGames.map((game) => {
                const Icon = game.icon;
                return (
                  <div
                    key={game.id}
                    className="relative bg-amber-50 border-4 border-amber-900 rounded-lg p-6 hover:shadow-xl transition-all cursor-pointer"
                    onClick={() => {
                      setSelectedGame(game);
                      setCurrentView('quest');
                    }}
                  >
                    {/* Game card */}
                    <div className="absolute top-2 right-2 w-20 h-20 bg-amber-900 opacity-5 rounded-full blur-xl"></div>
                    <div className="relative flex items-start gap-4 mb-4">
                      <div className="w-12 h-12 bg-gradient-to-br from-amber-700 to-amber-900 rounded flex items-center justify-center flex-shrink-0 border-2 border-amber-950">
                        <Icon className="w-7 h-7 text-amber-50" />
                      </div>
                      <div className="flex-1">
                        <h3 className="text-xl font-serif text-amber-900 mb-1">{game.name}</h3>
                        <p className="text-amber-800 text-sm italic">{game.description}</p>
                      </div>
                    </div>

                    {/* Progress bar */}
                    <div className="mb-4 bg-amber-100 p-3 rounded border border-amber-900 border-opacity-30">
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-amber-900 font-semibold">Current Quest:</span>
                        <span className="text-amber-800">{game.currentQuest}</span>
                      </div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-amber-900">Progress</span>
                        <span className="text-amber-800 font-semibold">{game.progress}%</span>
                      </div>
                      <div className="w-full bg-amber-300 h-2 rounded-full overflow-hidden border border-amber-900">
                        <div
                          className="h-full bg-gradient-to-r from-amber-700 to-amber-600"
                          style={{ width: `${game.progress}%` }}
                        ></div>
                      </div>
                      <div className="text-xs text-amber-800 mt-2 text-right">{game.playtime} inscribed</div>
                    </div>

                    {/* Difficulty and button */}
                    <div className="flex items-center justify-between">
                      <span className={`px-4 py-1 rounded-full text-sm font-semibold border-2 ${difficultyColors[game.difficulty]}`}>
                        {game.difficulty}
                      </span>
                      <button className="text-amber-800 hover:text-amber-900 font-serif font-semibold flex items-center gap-2">
                        Open Tome →
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Footer buttons */}
          <div className="flex justify-center gap-4 flex-wrap mt-8 pt-8 border-t-2 border-amber-900 border-opacity-30">
            <button
              onClick={() => setCurrentView('config')}
              className="bg-gradient-to-b from-amber-700 to-amber-900 text-amber-50 font-serif font-semibold py-3 px-8 rounded-lg flex items-center gap-2 transition-all shadow-lg border-4 border-amber-950 hover:from-amber-600 hover:to-amber-800"
            >
              <Settings className="w-5 h-5" />
              Grimoire Settings
            </button>
            <button
              onClick={() => setCurrentView('error')}
              className="bg-gradient-to-b from-amber-800 to-amber-900 text-amber-50 font-serif font-semibold py-3 px-8 rounded-lg flex items-center gap-2 transition-all shadow-lg border-4 border-amber-950 hover:from-amber-700 hover:to-amber-800"
            >
              <Shield className="w-5 h-5" />
              Test Fallback
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
