import React, { useState, useEffect, useRef } from 'react';
import { useArcadeStream } from '../hooks/useArcadeStream';
import { Scoreboard } from '../components/Scoreboard';
import { ContextSelector } from '../components/ContextSelector';
import { CodexDrawer } from '../components/CodexDrawer';
import { XPBar } from '../components/XPBar';
import { useAuth } from '../hooks/useAuth';
import { ProjectsPanel } from '../components/ProjectsPanel';
import { GameToast } from '../components/GameToast';

type World = {
  id: string;
  name: string;
  icon: string;
};

type Track = {
  id: string;
  world_id: string;
  name: string;
  source?: 'personal' | 'lab';
};

type Universe = {
  worlds: World[];
  tracks: Track[];
};

export default function DevUI({ isEmbedded = false }: { isEmbedded?: boolean }) {
  const [input, setInput] = useState('');

  // Context State
  const [context, setContext] = useState({
    mode: 'judge',
    world_id: 'world-python',
    track_id: 'applylens-backend'
  });

  // Universe Data
  const [universe, setUniverse] = useState<Universe>({ worlds: [], tracks: [] });

  // Codex State
  const [isCodexOpen, setIsCodexOpen] = useState(false);

  // Projects State
  const [isProjectsOpen, setIsProjectsOpen] = useState(false);

  // Generate a random session ID for demo purposes
  const [sid] = useState(() => `sess_${Math.random().toString(36).substr(2, 9)}`);

  // Auth
  const { user, login } = useAuth();

  const { messages, latestGrade, lastProgress, isStreaming, sendMessage, stopStream } = useArcadeStream(sid, user?.id || 'test');
  const bottomRef = useRef<HTMLDivElement>(null);

  // Fetch Universe Data
  useEffect(() => {
    fetch('/api/universe')
      .then(res => res.json())
      .then(data => {
        setUniverse(data);
        // Optional: Set default context if empty
        if (data.worlds.length > 0) {
          // Keep defaults or update
        }
      })
      .catch(err => console.error("Failed to load universe:", err));
  }, []);

  // Auto-scroll on new tokens
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming) return;
    sendMessage(input, context.mode, context.world_id, context.track_id);
    setInput('');
  };

  return (
    <div className="min-h-screen bg-black text-zinc-100 font-sans selection:bg-cyan-900 flex flex-col">

      {/* Header */}
      {!isEmbedded ? (
        <header className="border-b border-zinc-800 bg-zinc-950 px-4 py-2 flex justify-between items-center sticky top-0 z-30">

          {/* Left Side: Logo & Projects */}
          <div className="flex items-center gap-4">
            <div className="font-bold tracking-tight text-lg text-cyan-500">EVALFORGE <span className="text-zinc-600 text-xs">ARCADE</span></div>

            {/* Project Button (Visible when logged in) */}
            {user && (
              <button
                onClick={() => setIsProjectsOpen(true)}
                className="text-xs font-mono text-zinc-500 hover:text-cyan-400 flex items-center gap-1 transition-colors border-l border-zinc-800 pl-4"
              >
                <span className="text-lg leading-none">📁</span> PROJECTS
              </button>
            )}
          </div>

          {/* Right Side: XP, User, Codex */}
          <div className="flex items-center gap-6">
            {/* Only show XP if we have a user context (or just use 'test' default) */}
            <XPBar user={user?.id || 'test'} lastProgress={lastProgress} />

            {/* Login / User Badge */}
            {!user ? (
              <button
                onClick={login}
                className="text-xs bg-zinc-800 text-zinc-300 px-3 py-1.5 rounded hover:bg-zinc-700 font-bold transition-colors"
              >
                LOGIN (GITHUB)
              </button>
            ) : (
              <div className="flex items-center gap-2 group cursor-default">
                <img src={user.avatar_url} className="w-6 h-6 rounded-full border border-zinc-700 group-hover:border-cyan-500 transition-colors" alt="avatar" />
                <span className="text-xs font-mono text-zinc-500 group-hover:text-zinc-300">{user.name}</span>
              </div>
            )}

            <button
              onClick={() => setIsCodexOpen(true)}
              className="text-xs font-bold bg-zinc-900 border border-zinc-700 hover:border-cyan-500 text-zinc-300 px-3 py-1.5 rounded transition-all flex items-center gap-2"
            >
              📖 CODEX
            </button>
          </div>
        </header>
      ) : (
        /* Embedded Toolbar */
        <div className="absolute top-4 right-4 z-40 flex gap-2">
          {user && (
            <button
              onClick={() => setIsProjectsOpen(true)}
              className="bg-black/50 hover:bg-zinc-800 text-zinc-400 hover:text-cyan-400 border border-zinc-800 px-3 py-1.5 rounded text-xs font-mono transition-colors backdrop-blur"
            >
              📁 PROJECTS
            </button>
          )}
          <button
            onClick={() => setIsCodexOpen(true)}
            className="bg-black/50 hover:bg-zinc-800 text-zinc-400 hover:text-cyan-400 border border-zinc-800 px-3 py-1.5 rounded text-xs font-mono transition-colors backdrop-blur"
          >
            📖 CODEX
          </button>
          {!user && (
            <button
              onClick={login}
              className="bg-cyan-900/20 hover:bg-cyan-900/40 text-cyan-400 border border-cyan-900/50 px-3 py-1.5 rounded text-xs font-mono transition-colors backdrop-blur"
            >
              LOGIN
            </button>
          )}
        </div>
      )}

      <main className="flex-1 max-w-7xl mx-auto p-4 grid grid-cols-1 md:grid-cols-3 gap-6 w-full overflow-hidden">

        {/* Left Col: Scoreboard (Sticky) */}
        <div className="md:col-span-1 flex flex-col">
          <Scoreboard grade={latestGrade} />
        </div>

        {/* Right Col: Chat Interface */}
        <div className="md:col-span-2 flex flex-col bg-zinc-900/30 rounded-xl border border-zinc-800 overflow-hidden min-h-0">

          {/* Context Selector */}
          <ContextSelector
            context={context}
            setContext={setContext}
          />

          {/* Message List */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 && (
              <div className="text-center text-zinc-600 mt-20 font-mono text-sm">
                SYSTEM READY.<br />AWAITING INPUT...
              </div>
            )}

            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`max-w-[85%] rounded-lg p-3 text-sm leading-relaxed whitespace-pre-wrap ${msg.role === 'user'
                    ? 'bg-zinc-800 text-zinc-100 border border-zinc-700'
                    : 'bg-cyan-950/30 text-cyan-100 border border-cyan-900/50 font-mono'
                    }`}
                >
                  {msg.content}
                  {msg.role === 'assistant' && isStreaming && idx === messages.length - 1 && (
                    <span className="inline-block w-2 h-4 bg-cyan-500 ml-1 animate-blink align-middle" />
                  )}
                </div>
              </div>
            ))}
            <div ref={bottomRef} />
          </div>

          {/* Input Area */}
          <div className="p-4 border-t border-zinc-800 bg-zinc-950">
            <form onSubmit={handleSubmit} className="relative">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit(e);
                  }
                }}
                disabled={isStreaming}
                placeholder="Paste code or ask a question..."
                className="w-full bg-zinc-900 border border-zinc-700 rounded-lg p-3 pr-12 text-sm focus:outline-none focus:ring-1 focus:ring-cyan-500 resize-none h-24 font-mono transition-colors"
              />

              <div className="absolute bottom-3 right-3">
                {isStreaming ? (
                  <button
                    type="button"
                    onClick={stopStream}
                    className="px-3 py-1 bg-rose-900/50 text-rose-400 text-xs rounded hover:bg-rose-900 border border-rose-800 transition-colors"
                  >
                    STOP
                  </button>
                ) : (
                  <button
                    type="submit"
                    disabled={!input.trim()}
                    className="px-3 py-1 bg-cyan-900/50 text-cyan-400 text-xs rounded hover:bg-cyan-900 border border-cyan-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    RUN
                  </button>
                )}
              </div>
            </form>
          </div>

        </div>
      </main>

      {/* Drawers & Modals */}
      <CodexDrawer
        isOpen={isCodexOpen}
        onClose={() => setIsCodexOpen(false)}
        currentWorldId={context.world_id}
      />

      <ProjectsPanel
        user={user}
        isOpen={isProjectsOpen}
        onClose={() => setIsProjectsOpen(false)}
      />

      {/* Global Toast Notifications */}
      {!isEmbedded && <GameToast />}
    </div>
  );
}
