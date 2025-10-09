// src/components/GrimoireGame.tsx
import React, { useState } from 'react';
import { HomeView } from './views/HomeView';
import { QuestView } from './views/QuestView';
import { ConfigView } from './views/ConfigView';
import { ErrorView } from './views/ErrorView';
import { Screen, Game, Quest } from '../types';
import {
  Home, Settings, Book, Eye, Volume2, Monitor, Info, Scroll, Shield, Wand2, Gem,
  AlertTriangle, RotateCw, Sparkles, Feather
} from 'lucide-react';

export const GrimoireGame = () => {
  const [currentView, setCurrentView] = useState<Screen>('home');
  const [selectedTab, setSelectedTab] = useState<'gameplay' | 'audio' | 'display' | 'about'>('gameplay');
  const [hintFrequency, setHintFrequency] = useState(75);
  const [autoHints, setAutoHints] = useState(false);
  const [smartHints, setSmartHints] = useState(true);
  const [communityTips, setCommunityTips] = useState(true);
  const [selectedGame, setSelectedGame] = useState<Game | null>(null);
  const [showHint, setShowHint] = useState(false);

  const userGames: Game[] = [
    {
      id: 1,
      name: "The Elder Scrolls V: Skyrim",
      description: "Dragonborn rises in the north",
      difficulty: "Master",
      icon: Scroll,
      progress: 67,
      currentQuest: "Defeat Alduin",
      playtime: "145 hours"
    },
    {
      id: 2,
      name: "The Witcher 3: Wild Hunt",
      description: "Hunt for Ciri across the realms",
      difficulty: "Expert",
      icon: Wand2,
      progress: 42,
      currentQuest: "Find the Sunstone",
      playtime: "89 hours"
    },
    {
      id: 3,
      name: "Elden Ring",
      description: "Become the Elden Lord",
      difficulty: "Novice",
      icon: Gem,
      progress: 15,
      currentQuest: "Defeat Margit",
      playtime: "12 hours"
    },
    {
      id: 4,
      name: "Dark Souls III",
      description: "Link the First Flame",
      difficulty: "Adept",
      icon: Shield,
      progress: 58,
      currentQuest: "Soul of Cinder",
      playtime: "78 hours"
    }
  ];

  const [quests] = useState<Quest[]>([
    {
      id: 1,
      gameId: 1,
      name: 'Defeat the Shadow Lord',
      description: 'A legendary quest to defeat the ancient evil.',
      progress: 30
    }
  ]);

  return (
    <>
      {currentView === 'error' && <ErrorView setCurrentView={setCurrentView} />}
      {currentView === 'home' && (
        <HomeView
          setCurrentView={setCurrentView}
          userGames={userGames}
          setSelectedGame={setSelectedGame}
        />
      )}
      {currentView === 'quest' && selectedGame && (
        <QuestView
          game={selectedGame}
          setCurrentView={setCurrentView}
          quests={quests}
          showHint={showHint}
          setShowHint={setShowHint}
        />
      )}
      {currentView === 'config' && (
        <ConfigView
          setCurrentView={setCurrentView}
          selectedTab={selectedTab}
          setSelectedTab={setSelectedTab}
          hintFrequency={hintFrequency}
          setHintFrequency={setHintFrequency}
          autoHints={autoHints}
          setAutoHints={setAutoHints}
          smartHints={smartHints}
          setSmartHints={setSmartHints}
          communityTips={communityTips}
          setCommunityTips={setCommunityTips}
        />
      )}
    </>
  );
};
