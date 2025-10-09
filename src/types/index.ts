// src/types/index.ts
export type Screen = 'home' | 'quest' | 'config' | 'error';

export interface Game {
  id: number;
  name: string;
  description: string;
  difficulty: 'Master' | 'Expert' | 'Adept' | 'Novice';
  icon: React.ComponentType<{ className?: string }>;
  progress: number;
  currentQuest: string;
  playtime: string;
}

export interface Quest {
  id: number;
  gameId: number;
  name: string;
  description: string;
  progress: number;
}

export interface GameData {
  questProgress: number;
  questName: string;
  currentHint: string;
  hintConfidence: number;
  missedCollectibles: { found: number; total: number };
  communityTips: string[];
}
