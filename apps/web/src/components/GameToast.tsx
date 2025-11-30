import React, { useEffect, useState } from 'react';
import { useGameSocket } from '../hooks/useGameSocket';

export function GameToast() {
  const event = useGameSocket();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (event && (event.type === 'boss_spawn' || event.type === 'sync_complete')) {
      setVisible(true);
      // Auto-hide after 5 seconds
      const timer = setTimeout(() => setVisible(false), 5000);
      return () => clearTimeout(timer);
    }
  }, [event]);

  if (!visible || !event) return null;

  // Dynamic Styles based on event type
  const isBoss = event.type === 'boss_spawn';
  const isSync = event.type === 'sync_complete';

  if (!isBoss && !isSync) return null; // Ignore progress events here

  const styles = isBoss 
    ? "bg-red-950/90 border-red-500 shadow-[0_0_30px_rgba(220,38,38,0.5)]"
    : "bg-emerald-950/90 border-emerald-500 shadow-[0_0_30px_rgba(16,185,129,0.5)]";

  const icon = isBoss ? "🚨" : "✅";
  const titleColor = isBoss ? "text-red-400" : "text-emerald-400";

  return (
    <div className={`fixed bottom-8 left-1/2 transform -translate-x-1/2 z-50 animate-bounce-in border-2 rounded-lg p-4 flex items-center gap-4 max-w-lg ${styles}`}>
      <div className="text-3xl animate-bounce">{icon}</div>
      <div>
        <div className={`${titleColor} font-bold tracking-widest text-xs uppercase mb-1`}>
          {event.title}
        </div>
        <div className="text-white font-mono text-sm">
          {event.message}
        </div>
        {event.xp_bounty && (
          <div className="text-amber-400 text-xs font-bold mt-1">
            +{event.xp_bounty} XP Bounty!
          </div>
        )}
      </div>
    </div>
  );
}
