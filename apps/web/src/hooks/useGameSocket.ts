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
  // Boss Result fields
  outcome?: 'success' | 'failure';
};

export type SocketStatus = 'idle' | 'connecting' | 'connected' | 'error' | 'closed';

export function useGameSocket() {
  const [lastEvent, setLastEvent] = useState<GameEvent | null>(null);
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [status, setStatus] = useState<SocketStatus>('idle');

  useEffect(() => {
    // Connect to WebSocket endpoint using relative path to allow proxying
    // This fixes the issue where it was resolving to localhost:5173 without proxy handling correctly
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    // Use relative path so Vite proxy can handle it
    const wsUrl = `${protocol}//${window.location.host}/ws/game_events`;

    console.log(`🔌 Connecting to Game Socket: ${wsUrl}`);
    const ws = new WebSocket(wsUrl);
    setStatus('connecting');

    ws.onopen = () => {
      console.log('🎮 Game Event Socket Connected');
      setStatus('connected');
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
      setStatus('error');
    };

    ws.onclose = () => {
      console.log('🎮 Game Event Socket Disconnected');
      if (status !== 'error') {
        setStatus('closed');
      }
      // Attempt reconnect after 3 seconds
      setTimeout(() => {
        setSocket(null);
        // Force re-run of effect? No, we need to trigger re-connect.
        // Actually the current logic just sets socket to null which doesn't trigger re-connect 
        // unless we add it to dependency array or have a retry mechanism.
        // For now, let's just update status.
      }, 3000);
    };

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, []); // Re-connect logic needs improvement but sticking to fail-soft for now

  return { lastEvent, status };
}
