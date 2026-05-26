import React, { useState, useEffect, useRef } from 'react';
import { useArcadeStream, StreamContext } from '../hooks/useArcadeStream';
import { Scoreboard } from '../components/Scoreboard';
import { ContextSelector } from '../components/ContextSelector';

import { useAuth } from '../hooks/useAuth';
import { useSkills } from '../hooks/useSkills';
import { useBossStore } from '../store/bossStore';
import { useTrackWarp } from '../hooks/useTrackWarp';
import { BossPanel } from '../components/BossPanel';
import { CodexDrawer } from '../components/codex/CodexDrawer';
import { OracleTrackCard } from '../components/tracks/OracleTrackCard';
import { IntentOracleEvalButton } from '../components/devtools/IntentOracleEvalButton';
import { useGameStore } from '../store/gameStore';
import { WorkshopLayout, WorkshopMode } from '../layouts/WorkshopLayout';
import { BossHud } from '../components/BossHud';
// Sprint 22: LayoutProvider kept for test-mock compat; CyberdeckLayout/OrionLayout deleted.
import { LayoutProvider } from '../hooks/useCurrentLayout';
import { WorkshopGuide } from '../features/workshop/WorkshopGuide';
import { QuestBoard } from '../components/QuestBoard';
import { QuestIDE, QuestIDEPage } from '../components/quests/QuestIDE'; // New IDE Import
import { QuestSummary, fetchQuest } from '../lib/questsApi';
import { EventFeed } from '../components/EventFeed';
import { Routes, Route, Navigate, useLocation, useNavigate, Outlet, useSearchParams } from 'react-router-dom';
import { GettingStartedDialog } from '../features/tutorial/GettingStartedDialog';
import { STARTER_QUEST_ROUTE, TUTORIAL_STORAGE_KEY } from '../config/starter';
import { Terminal, ShieldAlert, BookOpen, Radio, HelpCircle } from 'lucide-react';
import { useUniverse } from '../hooks/useUniverse';
import { resolveSelectedProject } from '../lib/projectValidation';
import { PanelId } from '../features/workshop/workshopPanels';

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
  const location = useLocation();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams(); // ADDED
  const [input, setInput] = useState('');
  const [sid, setSid] = useState<string>('');
  const [isCodexOpen, setIsCodexOpen] = useState(false);
  const [codexRef, setCodexRef] = useState<string | null>(null);

  // Tutorial State
  const [showTutorial, setShowTutorial] = useState(false);

  useEffect(() => {
    const seen = window.localStorage.getItem(TUTORIAL_STORAGE_KEY);
    if (!seen) {
      setShowTutorial(true);
    }
  }, []);

  const handleTutorialOpenChange = (open: boolean) => {
    if (!open) {
      window.localStorage.setItem(TUTORIAL_STORAGE_KEY, "1");
    }
    setShowTutorial(open);
  };

  const handleStartStarterQuest = () => {
    window.localStorage.setItem(TUTORIAL_STORAGE_KEY, "1");
    setShowTutorial(false);
    navigate(STARTER_QUEST_ROUTE);
  };

  // View Mode REMOVED - using Routes now
  // const [viewMode, setViewMode] = useState<'board' | 'terminal'>('board');
  // const [activeQuest, setActiveQuest] = useState<QuestSummary | null>(null);

  // Local Context State
  const [context, setContext] = useState<StreamContext>({
    mode: 'judge',
    world_id: 'world-python',
    track_id: ''
  });

  // --- URL PANEL SYNC (NEW) ---
  useEffect(() => {
    const panel = searchParams.get('panel');
    // Only map known panels, ignore mapped legacy modes if needed
    if (panel && ['judge', 'explain', 'debug', 'codex'].includes(panel)) {
      // Only update if different to avoid loops
      if (context.mode !== panel) {
        setContext(prev => ({ ...prev, mode: panel as any }));
      }
    }
  }, [searchParams, context.mode]);


  // Global Project Validation
  const { universe } = useUniverse();
  const activeTrack = useGameStore((s) => s.activeTrack);
  const setActiveTrack = useGameStore((s) => s.setActiveTrack);

  useEffect(() => {
    if (universe && activeTrack) {
      const valid = resolveSelectedProject(activeTrack, universe);
      if (!valid) {
        console.log("🧹 Clearing stale project state (Global Guard):", activeTrack);
        setActiveTrack(null);
      }
    }
  }, [universe, activeTrack, setActiveTrack]);

  // --- WARP LOGIC (New) ---
  useTrackWarp((track) => {
    // 1. Map worldSlug to context world_id
    let targetWorldId = track.worldSlug;
    if (!targetWorldId.startsWith('world-')) {
      targetWorldId = `world-${targetWorldId}`;
    }

    // 2. Map trackSlug directly
    setContext(prev => ({
      ...prev,
      world_id: targetWorldId,
      track_id: track.trackSlug
    }));
  });

  // --- DEEP LINK LOGIC REMOVED (Handled by Routes now) ---

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

  // Boss store data
  const lastResult = useBossStore(s => s.lastResult);

  useEffect(() => {
    if (user) {
      // 1. Ensure Profile & Starter Quest (Idempotent)
      fetch('/api/profile/me')
        .then(r => {
          if (!r.ok) console.error("Profile sync failed", r.status);
        })
        .catch(e => console.error("Profile sync error", e));

      // 2. Restore Session
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

  // Force proceed after 5s to prevent infinite hanging
  const [forceProceed, setForceProceed] = useState(false);
  useEffect(() => {
    const timer = setTimeout(() => {
      if (loading) {
        console.warn("⚠️ Initialization timed out - Force proceeding");
        setForceProceed(true);
      }
    }, 5000);
    return () => clearTimeout(timer);
  }, [loading]);

  if (loading && !forceProceed) {
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
      onOpenCodex={() => { setIsCodexOpen(true); setCodexRef('codex:home'); }}
    />
  );


  // Render Outlet for routes to inject QuestBoard or QuestIDE
  const questPanel = (
    <div className="h-full flex flex-col bg-black/40 rounded-xl border border-zinc-800 overflow-hidden shadow-inner relative">
      {bossStatus === 'active' ? (
        <BossPanel onOpenCodex={() => { setIsCodexOpen(true); setCodexRef('codex:home'); }} />
      ) : (
        <div className="h-full">
          <Outlet />
        </div>
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

        {/* Agent Mode Switcher - REMOVED (Moved to WorkshopToolsPanel) */}
      </div>
    </div>
  );

  const codexPanel = (
    <div className="text-zinc-500 text-xs p-4">
      {/* Placeholder for Codex Widget if we want it inline */}
      <button onClick={() => { setIsCodexOpen(true); setCodexRef('codex:home'); }} className="text-cyan-400 hover:underline">
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

        {/* Workshop Guide (only shows if not dismissed) */}
        <WorkshopGuide />

        {/* Tutorial Help Button */}
        <button
          onClick={() => setShowTutorial(true)}
          data-testid="nav-getting-started"
          className="rounded-full bg-slate-900/80 border border-slate-700 p-2 text-slate-400 hover:text-emerald-400 hover:border-emerald-500/50 transition-all shadow-lg backdrop-blur-sm"
          title="Getting Started Guide"
        >
          <HelpCircle className="w-4 h-4" />
        </button>

      </div>
    ),
    integrityDelta: lastResult?.integrity_delta,
    bossHpDelta: lastResult?.boss_hp_delta,
    currentMode: context.mode as WorkshopMode,
    onModeChange: (mode: WorkshopMode) => {
      // Sync context AND URL
      setContext(prev => ({ ...prev, mode }));
      // Only update URL if it's a panel mode (not 'quest')
      if (['judge', 'explain', 'debug', 'codex'].includes(mode)) {
        setSearchParams(prev => {
          const copy = new URLSearchParams(prev);
          copy.set('panel', mode);
          return copy;
        });
      }
    },
    hasSkill: hasSkill,
  };

  // --- ROUTING ---
  // Replace manual layout switching with React Router

  const layoutContent = (
    <Routes>
      <Route path="/" element={<Navigate to="workshop" replace />} />

      {/* Workshop Route - Main workspace with nested Quest Routing */}
      <Route path="workshop" element={<WorkshopLayout {...commonProps} questPanel={<Outlet />} />}>
        <Route index element={<QuestBoard worldId={context.world_id} />} />
        <Route path="quests/:questId" element={<QuestIDEPage />} />
      </Route>

      {/* Sprint 22: CyberdeckLayout and OrionLayout deleted. Redirect legacy URLs. */}
      <Route path="orion" element={<Navigate to="/arcade/workshop" replace />} />
      <Route path="deck" element={<Navigate to="/arcade/workshop" replace />} />

      {/* Worlds Routing */}
      <Route path="worlds/:worldSlug">
        {/* Index: /worlds/foo -> Workshop (OrionLayout deleted Sprint 22) */}
        <Route index element={<Navigate to="/arcade/workshop" replace />} />

        {/* Sub-routes: /worlds/foo/quests/bar -> Workshop */}
        <Route path="quests/:questId" element={<WorkshopLayout {...commonProps} questPanel={<QuestIDEPage />} />} />
        <Route path="bosses/:bossSlug" element={<WorkshopLayout {...commonProps} questPanel={<BossPanel onOpenCodex={() => { setIsCodexOpen(true); setCodexRef('codex:home'); }} />} />} />
      </Route>

      {/* Projects Routing */}
      <Route path="projects/:projectSlug/*" element={<WorkshopLayout {...commonProps} />} />

    </Routes>
  );

  return (
    <>
      {layoutContent}

      {/* Tutorial Overlay */}
      <GettingStartedDialog
        open={showTutorial}
        onOpenChange={handleTutorialOpenChange}
        onStartStarterQuest={handleStartStarterQuest}
      />

      {/* Codex Drawer (Legacy Overlay REMOVED) */}


      {/* GOD MODE BANNER */}
      {godMode && (
        <div className="fixed bottom-2 right-2 rounded-lg px-3 py-2 text-xs bg-red-900/80 text-red-50 z-50 font-bold tracking-widest border border-red-500/50 shadow-lg animate-pulse">
          DEV GOD MODE: UNLOCKED
        </div>
      )}
    </>
  );
}

import { WorkshopCatalogProvider } from '../features/workshop/WorkshopCatalogContext';

export default function DevUI() {
  return (
    <LayoutProvider>
      <WorkshopCatalogProvider>
        <DevUIContent />
      </WorkshopCatalogProvider>
    </LayoutProvider>
  );
}
