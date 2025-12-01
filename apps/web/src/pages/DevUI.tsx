import React, { useState, useEffect, useRef } from 'react';
import { useArcadeStream, StreamContext } from '../hooks/useArcadeStream';
import { Scoreboard } from '../components/Scoreboard';
import { ContextSelector } from '../components/ContextSelector';
import { Terminal, ShieldAlert, BookOpen, Radio } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { useSkills } from '../hooks/useSkills'; // <--- Import
import { useBossStore } from '../store/bossStore';
import { useAgentStore } from '../store/agentStore';
import { BossPanel } from '../components/BossPanel';

// Map backend color names to Tailwind classes
const COLOR_MAP: Record<string, string> = {
  cyan: "text-cyan-400 border-cyan-500/30 bg-cyan-950/20",
  red: "text-red-500 border-red-500/30 bg-red-950/20",
  amber: "text-amber-400 border-amber-500/30 bg-amber-950/20",
  emerald: "text-emerald-400 border-emerald-500/30 bg-emerald-950/20",
  zinc: "text-zinc-400 border-zinc-500/30 bg-zinc-950/20", // Default
};

const ICON_MAP: Record<string, any> = {
  radar: Radio,
  eye: ShieldAlert,
  "book-open": BookOpen,
  wrench: Terminal, // Fallback for 'wrench' if not imported
  cpu: Terminal
};

export default function DevUI() {
  const { user } = useAuth();
  const { status: bossStatus } = useBossStore();
  const [input, setInput] = useState('');
  const [sid, setSid] = useState<string>('');

  useEffect(() => {
    if (user) {
      fetch('/api/session/active')
        .then(r => r.json())
        .then(session => {
          if (session.id) {
            console.log("💾 Restoring Session:", session.id);
            setSid(session.id);

            // Restore Context
            setContext(prev => ({
              ...prev,
              mode: session.mode || prev.mode,
              world_id: session.world_id || prev.world_id,
              track_id: session.track_id || prev.track_id
            }));

            // Restore Chat History
            if (session.history && Array.isArray(session.history)) {
              setMessages(session.history);
            }
          }
        })
        .catch(err => console.error("Failed to load session", err));
    }
  }, [user]);

  // Local Context State
  const [context, setContext] = useState<StreamContext>({
    mode: 'judge',
    world_id: 'world-python',
    track_id: 'applylens-backend'
  });

  const {
    messages,
    setMessages,
    latestGrade,
    isStreaming,
    sendMessage
  } = useArcadeStream(sid);
  const bottomRef = useRef<HTMLDivElement>(null);


  // Fetch skills for the logged-in user (or null)
  const { hasSkill } = useSkills(user);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming) return;
    sendMessage(input, context.mode, context.world_id, context.track_id, context.codex_id);
    setInput('');
  };

  return (
    <div className="h-full flex flex-col">

      {/* 1. Context Navigation (The Sub-Header) */}
      <div className="flex-none z-20 mb-4">
        <ContextSelector context={context} setContext={setContext} hasSkill={hasSkill} />
      </div>

      {/* 2. Main Workspace */}
      <div className="flex-1 p-4 grid grid-cols-1 lg:grid-cols-4 gap-6 overflow-hidden">

        {/* Left Column: Info/Score */}
        <div className="hidden lg:block lg:col-span-1 space-y-4 overflow-y-auto">
          {context.mode === 'judge' ? (
            <Scoreboard grade={latestGrade} />
          ) : (
            <div className="p-4 rounded-xl bg-zinc-900/50 border border-zinc-800 text-zinc-500 text-sm font-mono">
              <div className="text-[10px] uppercase tracking-widest text-zinc-600 mb-2">Active Protocol</div>
              <div className="text-xl text-cyan-400 font-bold capitalize mb-1">{context.mode}</div>
              <div className="text-xs border-t border-zinc-800 pt-2 mt-2">
                Session: {sid}
              </div>
            </div>
          )}
        </div>

        {/* Center/Right: Chat Terminal OR Boss Panel */}
        <div className="lg:col-span-3 flex flex-col bg-black/40 rounded-xl border border-zinc-800 overflow-hidden shadow-inner h-full">
          {bossStatus === 'active' ? (
            <BossPanel />
          ) : (
            <>
              {/* Chat History */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin scrollbar-thumb-zinc-700 scrollbar-track-transparent">
                {messages.length === 0 && (
                  <div className="h-full flex flex-col items-center justify-center text-zinc-700 font-mono text-sm opacity-50">
                    <div className="mb-4 text-4xl">_</div>
                    <div>SYSTEM READY</div>
                    <div>AWAITING INPUT...</div>
                  </div>
                )}

                {messages.map((msg, idx) => (
                  <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[90%] flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>

                      {/* --- NPC COMM LINK HEADER --- */}
                      {msg.role === 'assistant' && msg.npc && (
                        <div className="flex items-center gap-2 mb-1 px-1 opacity-0 animate-fade-in" style={{ animationDelay: '0.1s', animationFillMode: 'forwards' }}>
                          {/* Icon */}
                          {(() => {
                            const Icon = ICON_MAP[msg.npc.avatar_icon] || Terminal;
                            // Extract just the text color class
                            const colorClass = COLOR_MAP[msg.npc.color].split(' ')[0];
                            return <Icon className={`w-3 h-3 ${colorClass}`} />;
                          })()}

                          {/* Name & Title */}
                          <div className="flex items-baseline gap-2">
                            <span className={`text-[10px] font-bold tracking-widest uppercase ${COLOR_MAP[msg.npc.color].split(' ')[0]}`}>
                              {msg.npc.name}
                            </span>
                            <span className="text-[9px] text-zinc-600 font-mono uppercase tracking-wide hidden sm:inline">
                                  // {msg.npc.title}
                            </span>
                          </div>
                        </div>
                      )}
                      {/* --------------------------- */}

                      {/* Message Bubble */}
                      <div
                        className={`rounded p-3 text-sm leading-relaxed whitespace-pre-wrap font-mono relative group ${msg.role === 'user'
                          ? 'bg-zinc-800 text-zinc-200 border border-zinc-700'
                          : `text-cyan-100 border backdrop-blur-sm shadow-lg ${msg.npc ? COLOR_MAP[msg.npc.color] : 'bg-zinc-900/50 border-zinc-800'
                          }`
                          }`}
                      >
                        {msg.content}
                        {msg.role === 'assistant' && isStreaming && idx === messages.length - 1 && (
                          <span className="inline-block w-2 h-4 bg-current ml-1 animate-pulse align-middle opacity-50" />
                        )}
                      </div>
                    </div>
                  </div>
                ))}
                <div ref={bottomRef} />
              </div>

              {/* Input Area */}
              <div className="p-4 border-t border-zinc-800 bg-zinc-950/50">
                <form onSubmit={handleSubmit} className="relative group">
                  <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSubmit(e); } }}
                    disabled={isStreaming}
                    placeholder={hasSkill('syntax_highlighter') ? "Paste code or ask a question..." : "Paste code (Visuals Offline)..."}
                    className={`w-full bg-zinc-900/80 border border-zinc-700 rounded-lg p-3 pr-16 text-sm focus:outline-none focus:border-banana-400 focus:ring-1 focus:ring-banana-400/20 resize-none h-24 font-mono transition-all placeholder:text-zinc-700 ${hasSkill('syntax_highlighter') ? "text-zinc-100" : "text-zinc-500"}`}
                  />
                  <button
                    type="submit"
                    disabled={!input.trim() || isStreaming}
                    className="absolute bottom-3 right-3 text-[10px] font-bold bg-zinc-800 hover:bg-banana-500 hover:text-black text-zinc-400 px-3 py-1.5 rounded transition-all border border-zinc-700 disabled:opacity-0"
                  >
                    RUN_CMD
                  </button>
                </form>
              </div>
            </>
          )}
        </div>

      </div>
    </div>
  );
}
