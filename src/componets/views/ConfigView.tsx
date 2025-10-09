// src/components/views/ConfigView.tsx
import React from 'react';
import { Screen } from '../../types';
import { Home, Settings, Wand2, Volume2, Monitor, Info, Scroll, Sparkles, Gem } from 'lucide-react';

interface ConfigViewProps {
  setCurrentView: (view: Screen) => void;
  selectedTab: 'gameplay' | 'audio' | 'display' | 'about';
  setSelectedTab: (tab: 'gameplay' | 'audio' | 'display' | 'about') => void;
  hintFrequency: number;
  setHintFrequency: (value: number) => void;
  autoHints: boolean;
  setAutoHints: (value: boolean) => void;
  smartHints: boolean;
  setSmartHints: (value: boolean) => void;
  communityTips: boolean;
  setCommunityTips: (value: boolean) => void;
}

export const ConfigView: React.FC<ConfigViewProps> = ({
  setCurrentView,
  selectedTab,
  setSelectedTab,
  hintFrequency,
  setHintFrequency,
  autoHints,
  setAutoHints,
  smartHints,
  setSmartHints,
  communityTips,
  setCommunityTips
}) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-950 via-stone-950 to-stone-900 p-8 relative overflow-hidden">
      {/* Background texture */}
      <div className="absolute inset-0 opacity-5" style={{
        backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(139, 69, 19, 0.1) 2px, rgba(139, 69, 19, 0.1) 4px)'
      }}></div>

      {/* Main content */}
      <div className="max-w-5xl mx-auto relative">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <button
            onClick={() => setCurrentView('home')}
            className="bg-gradient-to-b from-amber-700 to-amber-900 text-amber-50 p-3 rounded-lg transition-all border-4 border-amber-950 hover:from-amber-600 hover:to-amber-800"
          >
            <Home className="w-6 h-6" />
          </button>
          <h1 className="text-4xl font-serif text-amber-100 flex items-center gap-3">
            <Settings className="w-8 h-8" />
            Grimoire Configuration
          </h1>
        </div>

        {/* Tab navigation */}
        <div className="flex gap-2 mb-6 bg-amber-900 rounded-lg p-2 border-4 border-amber-950">
          <button
            onClick={() => setSelectedTab('gameplay')}
            className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-all flex items-center justify-center gap-2 ${
              selectedTab === 'gameplay' ? 'bg-amber-100 text-amber-900' : 'text-amber-100 hover:bg-amber-800'
            }`}
          >
            <Wand2 className="w-5 h-5" />
            Gameplay
          </button>
          <button
            onClick={() => setSelectedTab('audio')}
            className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-all flex items-center justify-center gap-2 ${
              selectedTab === 'audio' ? 'bg-amber-100 text-amber-900' : 'text-amber-100 hover:bg-amber-800'
            }`}
          >
            <Volume2 className="w-5 h-5" />
            Audio
          </button>
          <button
            onClick={() => setSelectedTab('display')}
            className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-all flex items-center justify-center gap-2 ${
              selectedTab === 'display' ? 'bg-amber-100 text-amber-900' : 'text-amber-100 hover:bg-amber-800'
            }`}
          >
            <Monitor className="w-5 h-5" />
            Display
          </button>
          <button
            onClick={() => setSelectedTab('about')}
            className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-all flex items-center justify-center gap-2 ${
              selectedTab === 'about' ? 'bg-amber-100 text-amber-900' : 'text-amber-100 hover:bg-amber-800'
            }`}
          >
            <Info className="w-5 h-5" />
            About
          </button>
        </div>

        {/* Tab content */}
        {selectedTab === 'gameplay' && (
          <div className="bg-gradient-to-br from-amber-100 via-yellow-50 to-amber-100 rounded-lg p-8 shadow-2xl border-8 border-amber-900">
            <h2 className="text-3xl font-serif text-amber-900 mb-8">Gameplay Enchantments</h2>

            {/* Hint frequency slider */}
            <div className="mb-10">
              <div className="flex items-center gap-3 mb-4">
                <Scroll className="w-7 h-7 text-amber-800" />
                <h3 className="text-xl font-serif text-amber-900">Hint Frequency</h3>
              </div>
              <div className="relative mb-2">
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={hintFrequency}
                  onChange={(e) => setHintFrequency(Number(e.target.value))}
                  className="w-full h-3 bg-amber-300 rounded-full appearance-none cursor-pointer border border-amber-900"
                />
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-amber-800">Rare</span>
                <span className="text-amber-900 font-semibold">Medium</span>
                <span className="text-amber-800">Abundant</span>
              </div>
            </div>

            {/* Toggle switches */}
            <div className="h-px bg-amber-900 mb-8 opacity-30"></div>
            <div className="space-y-6">
              {/* Auto-hints toggle */}
              <div className="flex items-start justify-between p-4 bg-amber-50 rounded-lg border-2 border-amber-900">
                <div className="flex items-start gap-3">
                  <Sparkles className="w-6 h-6 text-amber-800 flex-shrink-0 mt-1" />
                  <div>
                    <h4 className="text-lg font-semibold text-amber-900 mb-1">Auto-Hints</h4>
                    <p className="text-amber-800 text-sm">Receive hints automatically when stuck</p>
                  </div>
                </div>
                <button
                  onClick={() => setAutoHints(!autoHints)}
                  className={`w-16 h-8 rounded-full transition-all border-2 relative ${
                    autoHints ? 'bg-amber-700 border-amber-900' : 'bg-stone-400 border-stone-600'
                  }`}
                >
                  <div className={`w-6 h-6 bg-white rounded-full transition-transform absolute top-0.5 ${
                    autoHints ? 'translate-x-8' : 'translate-x-1'
                  }`}></div>
                </button>
              </div>

              {/* Smart hints toggle */}
              <div className="flex items-start justify-between p-4 bg-amber-50 rounded-lg border-2 border-amber-900">
                <div className="flex items-start gap-3">
                  <Gem className="w-6 h-6 text-amber-800 flex-shrink-0 mt-1" />
                  <div>
                    <h4 className="text-lg font-semibold text-amber-900 mb-1">Smart Hints</h4>
                    <p className="text-amber-800 text-sm">Contextual hints based on your progress</p>
                  </div>
                </div>
                <button
                  onClick={() => setSmartHints(!smartHints)}
                  className={`w-16 h-8 rounded-full transition-all border-2 relative ${
                    smartHints ? 'bg-amber-700 border-amber-900' : 'bg-stone-400 border-stone-600'
                  }`}
                >
                  <div className={`w-6 h-6 bg-white rounded-full transition-transform absolute top-0.5 ${
                    smartHints ? 'translate-x-8' : 'translate-x-1'
                  }`}></div>
                </button>
              </div>

              {/* Community tips toggle */}
              <div className="flex items-start justify-between p-4 bg-amber-50 rounded-lg border-2 border-amber-900">
                <div className="flex items-start gap-3">
                  <Scroll className="w-6 h-6 text-amber-800 flex-shrink-0 mt-1" />
                  <div>
                    <h4 className="text-lg font-semibold text-amber-900 mb-1">Community Tips</h4>
                    <p className="text-amber-800 text-sm">Show tips from other adventurers</p>
                  </div>
                </div>
                <button
                  onClick={() => setCommunityTips(!communityTips)}
                  className={`w-16 h-8 rounded-full transition-all border-2 relative ${
                    communityTips ? 'bg-amber-700 border-amber-900' : 'bg-stone-400 border-stone-600'
                  }`}
                >
                  <div className={`w-6 h-6 bg-white rounded-full transition-transform absolute top-0.5 ${
                    communityTips ? 'translate-x-8' : 'translate-x-1'
                  }`}></div>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Other tabs (placeholders) */}
        {selectedTab === 'audio' && (
          <div className="bg-gradient-to-br from-amber-100 via-yellow-50 to-amber-100 rounded-lg p-8 shadow-2xl border-8 border-amber-900">
            <h2 className="text-3xl font-serif text-amber-900 mb-8">Audio Enchantments</h2>
            <p className="text-amber-800 text-center italic">Audio settings shall be inscribed here...</p>
          </div>
        )}
        {selectedTab === 'display' && (
          <div className="bg-gradient-to-br from-amber-100 via-yellow-50 to-amber-100 rounded-lg p-8 shadow-2xl border-8 border-amber-900">
            <h2 className="text-3xl font-serif text-amber-900 mb-8">Display Enchantments</h2>
            <p className="text-amber-800 text-center italic">Display settings shall be inscribed here...</p>
          </div>
        )}
        {selectedTab === 'about' && (
          <div className="bg-gradient-to-br from-amber-100 via-yellow-50 to-amber-100 rounded-lg p-8 shadow-2xl border-8 border-amber-900">
            <h2 className="text-3xl font-serif text-amber-900 mb-8">About This Grimoire</h2>
            <p className="text-amber-800 text-center italic">Information about the mystical grimoire shall be inscribed here...</p>
          </div>
        )}
      </div>
    </div>
  );
};
