// src/components/views/ErrorView.tsx
import React from 'react';
import { Screen } from '../../types';
import { Settings, Home, Sparkles, AlertTriangle, Feather, RotateCw, Gem } from 'lucide-react';

interface ErrorViewProps {
  setCurrentView: (view: Screen) => void;
}

export const ErrorView: React.FC<ErrorViewProps> = ({ setCurrentView }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-950 via-stone-950 to-stone-900 flex items-center justify-center p-8 relative overflow-hidden">
      {/* Background texture */}
      <div className="absolute inset-0 opacity-5" style={{
        backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(139, 69, 19, 0.1) 2px, rgba(139, 69, 19, 0.1) 4px)'
      }}></div>

      {/* Main content */}
      <div className="max-w-3xl w-full space-y-8 relative">
        {/* Error card */}
        <div className="relative bg-gradient-to-br from-amber-100 via-yellow-50 to-amber-100 shadow-2xl rounded-lg overflow-hidden border-8 border-amber-900">
          {/* Decorative elements */}
          <div className="absolute inset-0 opacity-20" style={{
            backgroundImage: 'radial-gradient(circle at 2px 2px, rgba(139, 69, 19, 0.3) 1px, transparent 0)',
            backgroundSize: '16px 16px'
          }}></div>
          <div className="absolute top-10 right-20 w-32 h-32 bg-amber-900 opacity-5 rounded-full blur-2xl"></div>
          <div className="absolute bottom-20 left-16 w-40 h-40 bg-amber-800 opacity-5 rounded-full blur-3xl"></div>

          {/* Error content */}
          <div className="relative p-12">
            <div className="text-center space-y-6">
              <div className="flex justify-center mb-4">
                <div className="relative">
                  <div className="w-24 h-24 rounded-full border-4 border-red-800 flex items-center justify-center bg-red-950 bg-opacity-30">
                    <Gem className="w-12 h-12 text-red-700" />
                  </div>
                  <div className="absolute inset-0 -m-6 border-2 border-amber-800 rounded-full opacity-30"></div>
                </div>
              </div>

              <div className="relative">
                <h1 className="text-5xl font-serif text-red-900 tracking-wide mb-2">Magic Disrupted</h1>
                <div className="flex justify-center gap-4 my-3">
                  <div className="w-20 h-0.5 bg-red-900"></div>
                  <Sparkles className="w-4 h-4 text-red-900" />
                  <div className="w-20 h-0.5 bg-red-900"></div>
                </div>
              </div>

              <p className="text-amber-900 text-lg italic leading-relaxed">
                Alas! The Grimoire's mystical connection hath faded into shadow...
              </p>

              <div className="border-4 border-red-900 bg-red-50 bg-opacity-50 rounded p-6 mt-6">
                <div className="flex items-start gap-4">
                  <AlertTriangle className="w-6 h-6 text-red-800 flex-shrink-0 mt-1" />
                  <p className="text-amber-900 text-left leading-relaxed">
                    The ancient servers art temporarily enchanted by chaos magic. Fear not, valiant adventurer - we possess backup wisdom inscribed upon sacred scrolls!
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Decorative corner */}
          <div className="absolute bottom-0 right-0 w-16 h-16 bg-amber-200 transform rotate-45 translate-x-8 translate-y-8 opacity-70"></div>
        </div>

        {/* Ancient wisdom card */}
        <div className="relative bg-gradient-to-br from-amber-100 via-yellow-50 to-amber-100 shadow-2xl rounded-lg overflow-hidden border-8 border-amber-900">
          <div className="p-8">
            <div className="flex items-start gap-4">
              <Feather className="w-8 h-8 text-amber-800 flex-shrink-0" />
              <div>
                <h2 className="text-3xl font-serif text-amber-900 mb-4">Ancient Wisdom</h2>
                <p className="text-amber-900 italic mb-2 leading-relaxed text-lg">
                  "Preserve thy game with diligence, most especially before decisions of great import"
                </p>
                <p className="text-amber-800 text-sm">
                  — Inscribed by the Guild of Anonymous Adventurers
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Action buttons */}
        <div className="space-y-4">
          <button
            onClick={() => setCurrentView('config')}
            className="w-full bg-gradient-to-b from-amber-700 to-amber-900 text-amber-50 font-serif font-semibold py-4 px-6 rounded-lg flex items-center justify-center gap-3 transition-all shadow-lg border-4 border-amber-950 hover:from-amber-600 hover:to-amber-800"
          >
            <Settings className="w-5 h-5" />
            Adjust Grimoire Settings
          </button>

          <button
            onClick={() => setCurrentView('home')}
            className="w-full bg-gradient-to-b from-amber-700 to-amber-900 text-amber-50 font-serif font-semibold py-4 px-6 rounded-lg flex items-center justify-center gap-3 transition-all shadow-lg border-4 border-amber-950 hover:from-amber-600 hover:to-amber-800"
          >
            <RotateCw className="w-5 h-5" />
            Attempt Magic Anew
          </button>

          <button className="w-full bg-gradient-to-b from-stone-800 to-stone-900 text-red-400 font-serif font-semibold py-4 px-6 rounded-lg flex items-center justify-center gap-3 transition-all shadow-lg border-4 border-stone-950">
            Abandon the Quest
          </button>
        </div>
      </div>
    </div>
  );
};
