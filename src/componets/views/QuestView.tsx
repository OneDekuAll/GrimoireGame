// src/components/views/QuestView.tsx
import React from 'react';
import { Screen, Game, Quest } from '../../types';
import { Home, Book, Eye, Sparkles, AlertTriangle, Shield } from 'lucide-react';

interface QuestViewProps {
  game: Game;
  setCurrentView: (view: Screen) => void;
  quests: Quest[];
  showHint: boolean;
  setShowHint: (show: boolean) => void;
}

export const QuestView: React.FC<QuestViewProps> = ({
  game,
  setCurrentView,
  quests,
  showHint,
  setShowHint
}) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-950 via-stone-950 to-stone-900 p-8 relative overflow-hidden">
      {/* Background texture */}
      <div className="absolute inset-0 opacity-5" style={{
        backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(139, 69, 19, 0.1) 2px, rgba(139, 69, 19, 0.1) 4px)'
      }}></div>

      {/* Main content */}
      <div className="max-w-7xl mx-auto relative">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <button
            onClick={() => setCurrentView('home')}
            className="bg-gradient-to-b from-amber-700 to-amber-900 text-amber-50 px-6 py-3 rounded-lg flex items-center gap-2 transition-all border-4 border-amber-950 font-serif hover:from-amber-600 hover:to-amber-800"
          >
            <Home className="w-5 h-5" />
            Return to Library
          </button>
          <h1 className="text-4xl font-serif text-amber-100 flex items-center gap-3">
            <Book className="w-8 h-8" />
            {game.name}
          </h1>
          <button className="bg-gradient-to-b from-amber-700 to-amber-900 text-amber-50 px-6 py-3 rounded-lg flex items-center gap-2 transition-all border-4 border-amber-950 font-serif hover:from-amber-600 hover:to-amber-800">
            <Book className="w-5 h-5" />
            Save All
          </button>
        </div>

        {/* Quest registry and scrying mirror */}
        <div className="relative bg-gradient-to-br from-amber-100 via-yellow-50 to-amber-100 rounded-lg shadow-2xl border-8 border-amber-900">
          {/* Divider */}
          <div className="absolute left-1/2 top-0 bottom-0 w-8 bg-gradient-to-r from-amber-900 from-opacity-20 via-amber-900 via-opacity-40 to-amber-900 to-opacity-20 transform -translate-x-1/2 z-10 opacity-20"></div>

          {/* Grid layout */}
          <div className="grid grid-cols-1 lg:grid-cols-2 relative">
            {/* Quest registry (left) */}
            <div className="p-8 lg:p-12 relative bg-gradient-to-r from-amber-100 to-amber-50">
              <h2 className="text-3xl font-serif text-amber-900 mb-6 text-center pb-4 border-b-2 border-amber-900 border-opacity-30">
                Quest Registry
              </h2>

              {/* Current quest */}
              <div className="bg-amber-100 border-2 border-amber-900 rounded-lg p-6 mb-6">
                <div className="flex items-start justify-between mb-4">
                  <h3 className="text-xl font-serif text-amber-900">{game.currentQuest}</h3>
                  <Shield className="w-5 h-5 text-amber-800" />
                </div>
                <p className="text-amber-800 text-sm mb-4 italic">Main questline progression</p>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-amber-900">Progress</span>
                    <span className="text-amber-800 font-semibold">{game.progress}%</span>
                  </div>
                  <div className="w-full bg-amber-300 h-3 rounded-full overflow-hidden border border-amber-900">
                    <div
                      className="h-full bg-gradient-to-r from-amber-700 to-amber-600"
                      style={{ width: `${game.progress}%` }}
                    ></div>
                  </div>
                </div>
              </div>

              {/* Other quests */}
              {quests.filter(q => q.gameId === game.id).map(quest => (
                <div key={quest.id} className="bg-amber-100 border-2 border-amber-900 rounded-lg p-6 mb-4">
                  <div className="flex items-start justify-between mb-4">
                    <h3 className="text-xl font-serif text-amber-900">{quest.name}</h3>
                    <button className="text-red-800 hover:text-red-900">
                      <AlertTriangle className="w-5 h-5" />
                    </button>
                  </div>
                  <p className="text-amber-800 text-sm mb-4">{quest.description}</p>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-amber-900">Progress</span>
                      <span className="text-amber-800 font-semibold">{quest.progress}%</span>
                    </div>
                    <div className="w-full bg-amber-300 h-3 rounded-full overflow-hidden border border-amber-900">
                      <div
                        className="h-full bg-gradient-to-r from-amber-700 to-amber-600"
                        style={{ width: `${quest.progress}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}

              {/* Add new quest */}
              <div className="border-2 border-green-800 bg-green-50 rounded-lg p-6 mt-6">
                <h3 className="text-2xl font-serif text-green-900 mb-4">Inscribe New Quest</h3>
                <input
                  type="text"
                  placeholder="Quest name..."
                  className="w-full bg-white border-2 border-amber-900 text-amber-900 placeholder-amber-600 px-4 py-3 rounded mb-3 focus:border-amber-700 focus:outline-none"
                />
                <textarea
                  placeholder="Quest details..."
                  rows={3}
                  className="w-full bg-white border-2 border-amber-900 text-amber-900 placeholder-amber-600 px-4 py-3 rounded mb-4 focus:border-amber-700 focus:outline-none resize-none"
                ></textarea>
                <button className="w-full bg-gradient-to-b from-green-700 to-green-900 text-green-50 py-3 rounded-lg font-semibold transition-all border-2 border-green-950 hover:from-green-600 hover:to-green-800">
                  + Add Quest
                </button>
              </div>
            </div>

            {/* Scrying mirror (right) */}
            <div className="p-8 lg:p-12 relative bg-gradient-to-l from-amber-100 to-amber-50">
              <h2 className="text-3xl font-serif text-amber-900 mb-6 text-center pb-4 border-b-2 border-amber-900 border-opacity-30">
                Scrying Mirror
              </h2>

              <div className="border-4 border-amber-900 rounded-lg p-12 bg-gradient-to-br from-amber-200 to-amber-100 min-h-96 flex flex-col items-center justify-center">
                <div className="w-32 h-32 rounded-full bg-amber-900 bg-opacity-20 flex items-center justify-center mb-6 border-4 border-amber-900">
                  <Eye className="w-16 h-16 text-amber-800" />
                </div>
                <p className="text-amber-800 text-lg mb-2">The scrying mirror awaits...</p>
                <p className="text-amber-700 text-sm mb-6">Click "Begin Scrying" to view your screen</p>
                <button
                  onClick={() => setShowHint(!showHint)}
                  className="bg-gradient-to-b from-green-700 to-green-900 text-green-50 px-8 py-3 rounded-lg font-semibold transition-all flex items-center gap-2 border-4 border-green-950 hover:from-green-600 hover:to-green-800"
                >
                  <Eye className="w-5 h-5" />
                  Begin Scrying
                </button>

                {showHint && (
                  <div className="mt-6 bg-yellow-100 border-4 border-yellow-700 rounded-lg p-6 animate-fade-in">
                    <div className="flex items-center gap-3 mb-3">
                      <Sparkles className="w-6 h-6 text-yellow-700" />
                      <h4 className="font-serif text-xl text-yellow-900">Ancient Hint</h4>
                    </div>
                    <p className="text-yellow-900 italic">"Check behind the waterfall for a hidden passage!"</p>
                    <p className="text-yellow-800 text-sm mt-2">90% of adventurers found this helpful</p>
                  </div>
                )}
              </div>
              <button className="w-full mt-6 bg-gradient-to-b from-stone-800 to-stone-900 text-yellow-600 py-3 rounded-lg font-semibold transition-all flex items-center justify-center gap-2 border-2 border-stone-950">
                <Eye className="w-5 h-5" />
                Mirror Dormant
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
