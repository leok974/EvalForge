import React, { useEffect, useState } from 'react';
import { useGameSocket } from '../hooks/useGameSocket';

export function GameToast() {
  const event = useGameSocket();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (event) {
      setVisible(true);
      const timer = setTimeout(() => setVisible(false), 8000);
      return () => clearTimeout(timer);
    }
  }, [event]);

  if (!visible || !event) return null;

  // --- STYLE LOGIC ---
  let styles = "bg-zinc-900 border-zinc-700";
  let icon = "ℹ️";
  let titleColor = "text-white";

  if (event.type === 'boss_spawn') {
    styles = "bg-red-950/90 border-red-500 shadow-[0_0_30px_rgba(220,38,38,0.5)]";
    icon = "🚨";
    titleColor = "text-red-400";
  }
  else if (event.type === 'sync_complete') {
    styles = "bg-emerald-950/90 border-emerald-500 shadow-[0_0_30px_rgba(16,185,129,0.5)]";
    icon = "✅";
    titleColor = "text-emerald-400";
  }
  else if (event.type === 'achievement') { // <--- NEW TYPE
    // Gold / Legendary Styling
    styles = "bg-black/95 border-2 border-banana-400 shadow-[0_0_50px_rgba(250,204,21,0.4)]";
    icon = "🏆";
    titleColor = "text-banana-400";
  }

  // Handle Achievement Payload Structure
  const title = event.type === 'achievement' ? event.badge?.name : event.title;
  const message = event.type === 'achievement' ? event.badge?.description : event.message;
  const subtext = event.type === 'achievement' && event.badge?.xp_bonus
    ? `+${event.badge.xp_bonus} XP BONUS`
    : (event.xp_bounty ? `BOUNTY: ${event.xp_bounty} XP` : null);

  return (
    <div className={`fixed bottom-8 left-1/2 transform -translate-x-1/2 z-50 animate-bounce-in rounded-lg p-4 flex items-center gap-4 max-w-lg ${styles}`}>
      <div className="text-4xl animate-bounce">{event.type === 'achievement' ? event.badge?.icon || icon : icon}</div>
      <div>
        <div className="text-[10px] uppercase tracking-widest text-zinc-400 mb-1">
          {event.type === 'achievement' ? 'ACHIEVEMENT UNLOCKED' : 'SYSTEM ALERT'}
        </div>
        <div className={`font-bold text-lg font-mono leading-none mb-1 ${titleColor}`}>
          {title}
        </div>
        <div className="text-zinc-300 text-xs font-sans">
          {message}
        </div>
        {subtext && (
          <div className="mt-2 inline-block bg-white/10 text-white text-[9px] px-2 py-0.5 rounded font-bold border border-white/10">
            {subtext}
          </div>
        )}
      </div>
    </div>
  );
}
