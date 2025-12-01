import { useEffect, useState } from 'react';

export type GameEvent = {
  type: 'boss_spawn' | 'sync_progress' | 'sync_complete' | 'achievement' | 'quest_complete';
  title?: string;
  message?: string;
  // Sync specific fields
  project_id?: string;
  percent?: number;
  eta_seconds?: number;
  xp_bounty?: number;
  // Boss spawn fields
  boss_id?: string;
  name?: string;
  difficulty?: string;
  duration_seconds?: number;
  hp_penalty_on_fail?: number;
  base_xp_reward?: number;
  // Achievement specific fields
  badge?: {
    name: string;
    description: string;
    icon: string;
    rarity: string;
    xp_bonus: number;
  };
};

export function useGameSocket() {
  const [lastEvent, setLastEvent] = useState<GameEvent | null>(null);
  const [socket, setSocket] = useState<WebSocket | null>(null);

  useEffect(() => {
    // Connect to WebSocket endpoint
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//${window.location.host}/ws/game_events`);

    ws.onopen = () => {
      console.log('🎮 Game Event Socket Connected');
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setLastEvent(data);
      } catch (e) {
        console.error('Failed to parse game event:', e);
      }
    };

    ws.onerror = (error) => {
      console.error('Game Socket Error:', error);
    };

    ws.onclose = () => {
      console.log('🎮 Game Event Socket Disconnected');
      // Attempt reconnect after 3 seconds
      setTimeout(() => {
        setSocket(null);
      }, 3000);
    };

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, []);

  return lastEvent;
}
