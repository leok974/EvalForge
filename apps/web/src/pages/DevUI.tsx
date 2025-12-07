import React, { useState, useEffect, useRef } from 'react';
import { useArcadeStream, StreamContext } from '../hooks/useArcadeStream';
import { Scoreboard } from '../components/Scoreboard';
import { ContextSelector } from '../components/ContextSelector';
import { Terminal, ShieldAlert, BookOpen, Radio } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { useSkills } from '../hooks/useSkills';
import { useBossStore } from '../store/bossStore';
import { useTrackWarp } from '../hooks/useTrackWarp';
import { BossPanel } from '../components/BossPanel';
import { CodexDrawer } from '../components/CodexDrawer';
import { OracleTrackCard } from '../components/tracks/OracleTrackCard';
import { IntentOracleEvalButton } from '../components/devtools/IntentOracleEvalButton';
import { useGameStore } from '../store/gameStore';
import { WorkshopLayout, WorkshopMode } from '../layouts/WorkshopLayout';
import { CyberdeckLayout } from '../layouts/CyberdeckLayout';
import { OrionLayout } from '../layouts/OrionLayout';
import { BossHud } from '../components/BossHud';
import { LayoutSwitcher } from '../components/LayoutSwitcher';
import { LayoutProvider, useCurrentLayout } from '../hooks/useCurrentLayout';
import { WorkshopGuide } from '../features/workshop/WorkshopGuide';
import { QuestBoard } from '../components/QuestBoard';
import { EventFeed } from '../components/EventFeed';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';

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

function DevUIContent() {
  const { user, login, loading } = useAuth();
  const { status: bossStatus } = useBossStore();
  const { layout } = useCurrentLayout();
  const location = useLocation();
  const [input, setInput] = useState('');
  const [sid, setSid] = useState<string>('');
  const [isCodexOpen, setIsCodexOpen] = useState(false);

  // View Mode for Workbench (Quest Board vs Terminal) - MUST be before early returns
  const [viewMode, setViewMode] = useState<'board' | 'terminal'>('board');

  // Local Context State
  const [context, setContext] = useState<StreamContext>({
    mode: 'judge',
    world_id: 'world-python',
    track_id: 'applylens-backend'
  });

  // --- WARP LOGIC (New) ---
  useTrackWarp((track) => {
    // 1. Map worldSlug to context world_id
    // If track.worldSlug is 'python', context usually expects 'world-python'.
    let targetWorldId = track.worldSlug;
    if (!targetWorldId.startsWith('world-')) {
      targetWorldId = `world-${targetWorldId}`;
    }

    // 2. Map trackSlug directly (assuming context.track_id uses slugs like 'python-basics')
    setContext(prev => ({
      ...prev,
      world_id: targetWorldId,
      track_id: track.trackSlug // Ensure QuestBoard respects this
    }));

    // Optionally switch view to 'board' to see the quests
    setViewMode('board');
  });

  const {
    messages,
    setMessages,
    latestGrade,
    isStreaming,
    sendMessage
  } = useArcadeStream(sid, user?.id || 'guest');
  const bottomRef = useRef<HTMLDivElement>(null);

  // Fetch skills for the logged-in user (or null)
  const { hasSkill, godMode } = useSkills(user);

  // Boss store data - MUST be before early returns
  const lastResult = useBossStore(s => s.lastResult);

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

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center bg-black text-zinc-500 font-mono text-sm animate-pulse">
        INITIALIZING LINK...
      </div>
    );
  }

  if (!user) {
    return (
      <div className="h-full flex flex-col items-center justify-center bg-black text-zinc-400 font-mono space-y-6">
        <div className="text-4xl font-bold text-cyan-500 tracking-widest glitch-text">EVALFORGE</div>
        <div className="text-xs uppercase tracking-[0.2em] text-zinc-600">Secure Uplink Required</div>

        <button
          onClick={login}
          className="group relative px-8 py-3 bg-zinc-900 border border-cyan-900/50 hover:border-cyan-500/50 text-cyan-400 text-xs font-bold tracking-widest uppercase transition-all hover:bg-cyan-950/30"
        >
          <span className="absolute inset-0 w-full h-full bg-cyan-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
          Initialize Session
        </button>
      </div>
    );
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming) return;
    sendMessage(input, context.mode, context.world_id, context.track_id, context.codex_id);
    setInput('');
  };

  // --- COMPONENT SLOTS ---

  const bossHud = <BossHud />;

  const worldSelector = (
    <ContextSelector
      context={context}
      setContext={setContext}
      hasSkill={hasSkill}
      onOpenCodex={() => setIsCodexOpen(true)}
    />
  );


  const questPanel = (
    <div className="h-full flex flex-col bg-black/40 rounded-xl border border-zinc-800 overflow-hidden shadow-inner relative">
      {/* View Switcher (Floating) */}
      <div className="absolute top-2 right-2 z-10 flex gap-1 bg-black/60 p-1 rounded-lg border border-zinc-800 backdrop-blur-sm">
        <button
          onClick={() => setViewMode('board')}
          className={`px-2 py-1 text-[10px] uppercase tracking-wider font-bold rounded ${viewMode === 'board' ? 'bg-cyan-900/50 text-cyan-400 border border-cyan-500/30' : 'text-zinc-500 hover:text-zinc-300'
            }`}
        >
          Quests
        </button>
        <button
          onClick={() => setViewMode('terminal')}
          className={`px-2 py-1 text-[10px] uppercase tracking-wider font-bold rounded ${viewMode === 'terminal' ? 'bg-cyan-900/50 text-cyan-400 border border-cyan-500/30' : 'text-zinc-500 hover:text-zinc-300'
            }`}
        >
          Terminal
        </button>
      </div>

      {bossStatus === 'active' ? (
        <BossPanel onOpenCodex={() => setIsCodexOpen(true)} />
      ) : viewMode === 'board' ? (
        <div className="p-4 h-full overflow-hidden">
          <QuestBoard
            worldId={context.world_id}
            onOpenQuest={(quest) => {
              // Switch to terminal view when a quest is opened
              setViewMode('terminal');
              // Optionally: We could also set context to match the quest's track/world if needed
              // setContext(prev => ({ ...prev, track_id: quest.track_id }));
            }}
          />
        </div>
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

          {/* Input Area - GATED */}
          <div className="p-4 border-t border-zinc-800 bg-zinc-950/50">
            <form onSubmit={handleSubmit} className="relative group">
              {hasSkill('syntax_highlighter') ? (
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSubmit(e); } }}
                  disabled={isStreaming}
                  placeholder="Paste code or ask a question..."
                  className="w-full bg-zinc-900/80 border border-zinc-700 rounded-lg p-3 pr-16 text-sm focus:outline-none focus:border-banana-400 focus:ring-1 focus:ring-banana-400/20 resize-none h-24 font-mono transition-all placeholder:text-zinc-700 text-zinc-100"
                />
              ) : (
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSubmit(e); } }}
                  disabled={isStreaming}
                  placeholder="// RAW MODE: Syntax Highlighting Offline. Unlock 'Optical Enhancer' in Cybernetics Lab."
                  className="w-full bg-zinc-900/80 border border-zinc-700 rounded-lg p-3 pr-16 text-sm focus:outline-none focus:border-zinc-600 resize-none h-24 font-mono transition-all placeholder:text-zinc-500 text-zinc-500"
                />
              )}

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
  );

  const projectPanel = (
    <div className="space-y-4">
      {/* Info/Score */}
      <div className="space-y-4">
        {context.mode === 'judge' ? (
          <>
            <Scoreboard grade={latestGrade} />
            {/* Oracle Track Card */}
            {context.world_id === 'world-oracle' && (
              <OracleTrackCard
                state={{ invocation: 'completed', grounding: 'available', boss: 'locked' }}
                onOpenBossCodex={() => setIsCodexOpen(true)}
              />
            )}
          </>
        ) : (
          <div className="p-4 rounded-xl bg-zinc-900/50 border border-zinc-800 text-zinc-500 text-sm font-mono">
            <div className="text-[10px] uppercase tracking-widest text-zinc-600 mb-2">Active Protocol</div>
            <div className="text-xl text-cyan-400 font-bold capitalize mb-1">{context.mode}</div>
            <div className="text-xs border-t border-zinc-800 pt-2 mt-2">
              Session: {sid}
            </div>
          </div>
        )}

        {/* Dev Tools / Eval Button */}
        {godMode && (
          <IntentOracleEvalButton />
        )}

        {/* Agent Mode Switcher - GATED (Hidden in Workshop/Orion as they have their own HUDs) */}
        {layout !== 'workshop' && layout !== 'orion' && !location.pathname.includes('/workshop') && !location.pathname.includes('/orion') && (
          <div className="flex gap-2">
            <button
              onClick={() => setContext(prev => ({ ...prev, mode: 'judge' }))}
              className={`flex-1 py-2 text-xs font-bold tracking-widest border transition-all ${context.mode === 'judge'
                ? 'bg-red-950/40 border-red-500 text-red-400 shadow-[0_0_10px_rgba(239,68,68,0.2)]'
                : 'bg-black border-zinc-800 text-zinc-600 hover:border-zinc-700'
                }`}
            >
              JUDGE
            </button>
            <button
              onClick={() => hasSkill('agent_explain') && setContext(prev => ({ ...prev, mode: 'explain' }))}
              disabled={!hasSkill('agent_explain')}
              className={`flex-1 py-2 text-xs font-bold tracking-widest border transition-all ${context.mode === 'explain'
                ? 'bg-amber-950/40 border-amber-500 text-amber-400 shadow-[0_0_10px_rgba(245,158,11,0.2)]'
                : !hasSkill('agent_explain')
                  ? 'bg-black border-zinc-900 text-zinc-800 cursor-not-allowed opacity-50'
                  : 'bg-black border-zinc-800 text-zinc-600 hover:border-zinc-700'
                }`}
            >
              EXPLAIN {!hasSkill('agent_explain') && '🔒'}
            </button>
            <button
              onClick={() => hasSkill('agent_debug') && setContext(prev => ({ ...prev, mode: 'debug' }))}
              disabled={!hasSkill('agent_debug')}
              className={`flex-1 py-2 text-xs font-bold tracking-widest border transition-all ${context.mode === 'debug'
                ? 'bg-emerald-950/40 border-emerald-500 text-emerald-400 shadow-[0_0_10px_rgba(16,185,129,0.2)]'
                : !hasSkill('agent_debug')
                  ? 'bg-black border-zinc-900 text-zinc-800 cursor-not-allowed opacity-50'
                  : 'bg-black border-zinc-800 text-zinc-600 hover:border-zinc-700'
                }`}
            >
              DEBUG {!hasSkill('agent_debug') && '🔒'}
            </button>
          </div>
        )}
      </div>
    </div>
  );

  const codexPanel = (
    <div className="text-zinc-500 text-xs p-4">
      {/* Placeholder for Codex Widget if we want it inline */}
      <button onClick={() => setIsCodexOpen(true)} className="text-cyan-400 hover:underline">
        Open Codex Drawer
      </button>
    </div>
  );

  const activityFeed = (
    <EventFeed />
  );

  // --- LAYOUT SWITCHING ---

  const commonProps = {
    bossHud,
    worldSelector,
    questPanel,
    projectPanel,
    codexPanel,
    activityFeed,
    extraTopRight: (
      <div className="flex flex-col items-end gap-2">
        {/* Layout Switcher Tile */}
        <div
          className={`
              rounded-2xl border border-amber-500/50 bg-slate-950/90
              px-2.5 py-2 text-[11px]
              shadow-[0_16px_30px_rgba(245,158,11,0.4)]
              backdrop-blur-xl
              transform rotate-1 hover:-rotate-0.5 transition-transform duration-150
            `}
        >
          <LayoutSwitcher />
        </div>

        {/* Workshop Guide (only shows if not dismissed) */}
        {layout === 'workshop' && <WorkshopGuide />}
      </div>
    ),
    integrityDelta: lastResult?.integrity_delta,
    bossHpDelta: lastResult?.boss_hp_delta,
    currentMode: context.mode as WorkshopMode,
    onModeChange: (mode: WorkshopMode) => setContext(prev => ({ ...prev, mode })),
    hasSkill: hasSkill,
  };

  // --- ROUTING ---
  // Replace manual layout switching with React Router


  const layoutContent = (
    <Routes>
      {/* Default / Dashboard route -> Workshop or Cyberdeck? 
          User requested: 
            index → WorkshopLayout 
            top-level workshop → WorkshopLayout
            top-level orion → OrionLayout
      */}
      <Route path="/" element={<Navigate to="/workshop" replace />} />

      <Route path="/workshop" element={<WorkshopLayout {...commonProps} />} />
      <Route path="/orion" element={<OrionLayout />} />

      {/* Cyberdeck fallback or explicit route */}
      <Route path="/deck" element={
        <CyberdeckLayout>
          <div className="h-full flex flex-col">
            {/* 1. Context Navigation */}
            <div className="flex-none z-20 mb-4">
              {worldSelector}
            </div>

            {/* 2. Main Workspace */}
            <div className="flex-1 p-4 grid grid-cols-1 lg:grid-cols-4 gap-6 overflow-hidden">
              {/* Left Column: Info/Score */}
              <div className="hidden lg:block lg:col-span-1 space-y-4 overflow-y-auto">
                {projectPanel}
              </div>

              {/* Center/Right: Chat Terminal OR Boss Panel */}
              <div className="lg:col-span-3 flex flex-col bg-black/40 rounded-xl border border-zinc-800 overflow-hidden shadow-inner h-full">
                {questPanel}
              </div>
            </div>
          </div>
        </CyberdeckLayout>
      } />

      {/* Worlds Routing */}
      <Route path="/worlds/:worldSlug">
        {/* Index: /worlds/foo -> Orion Map */}
        <Route index element={<OrionLayout />} />

        {/* Sub-routes: /worlds/foo/quests/bar -> Workshop */}
        <Route path="quests/:questId" element={<WorkshopLayout {...commonProps} />} />
        <Route path="bosses/:bossSlug" element={<WorkshopLayout {...commonProps} />} />
      </Route>

      {/* Projects Routing - Similar pattern if needed later, but keeping simple for now */}
      <Route path="/projects/:projectSlug/*" element={<WorkshopLayout {...commonProps} />} />

    </Routes>
  );

  return (
    <>
      {layoutContent}

      {/* Codex Drawer (Overlay) */}
      <CodexDrawer
        isOpen={isCodexOpen}
        onClose={() => setIsCodexOpen(false)}
        currentWorldId={context.world_id || 'world-python'}
      />

      {/* GOD MODE BANNER */}
      {godMode && (
        <div className="fixed bottom-2 right-2 rounded-lg px-3 py-2 text-xs bg-red-900/80 text-red-50 z-50 font-bold tracking-widest border border-red-500/50 shadow-lg animate-pulse">
          DEV GOD MODE: UNLOCKED
        </div>
      )}
    </>
  );
}

export default function DevUI() {
  return (
    <LayoutProvider>
      <DevUIContent />
    </LayoutProvider>
  );
}
