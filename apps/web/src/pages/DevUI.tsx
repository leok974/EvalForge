/**
 * EvalForge Dev UI - Interactive testing interface
 */
import React, { useEffect, useRef, useState } from "react";
import { Scoreboard, GradeData } from "../components/Scoreboard";
import { getSessionStateFields } from "../lib/api";
import { ThemeToggle } from "../components/ThemeToggle";

export default function DevUI() {
  const [sessionId, setSessionId] = useState<string>("");
  const [log, setLog] = useState<string[]>([]);
  const [grade, setGrade] = useState<GradeData | undefined>(undefined);
  const [baseUrl] = useState<string>(() =>
    (typeof window !== "undefined" ? window.location.origin : "http://127.0.0.1:19010")
  );
  const [loadingGrade, setLoadingGrade] = useState(false);
  const pollTimer = useRef<number | null>(null);

  const append = (s: string) => setLog((L) => [...L, s]);
  
  const stopPoll = () => {
    if (pollTimer.current) {
      window.clearInterval(pollTimer.current);
      pollTimer.current = null;
    }
  };
  
  useEffect(() => stopPoll, []);

  async function refreshScoreboard(manual = false) {
    if (!sessionId) return;
    try {
      setLoadingGrade(true);
      const data = await getSessionStateFields(baseUrl, sessionId, ["last_grade", "track"]);
      if (data?.last_grade) {
        setGrade(data.last_grade);
        if (manual) append("🔁 Scoreboard refreshed.");
      } else if (manual) {
        append("ℹ️ No grade yet. Trigger Judge by submitting code.");
      }
    } catch (e: any) {
      append(`⚠️ Scoreboard fetch failed: ${e.message || e}`);
    } finally {
      setLoadingGrade(false);
    }
  }

  async function createSession() {
    const res = await fetch(`${baseUrl}/apps/arcade_app/users/test/sessions`, { 
      method: "POST", 
      headers: { "Content-Length": "0" }
    });
    const data = await res.json();
    setSessionId(data.id);
    append(`🧪 Session created: ${data.id}`);
    // Brief scoreboard refresh on create (no grade expected yet)
    setTimeout(() => refreshScoreboard(false), 200);
  }

  async function sendMessage(message: string) {
    if (!sessionId) return append("⚠️ Create a session first.");
    const res = await fetch(`${baseUrl}/apps/arcade_app/users/test/sessions/${sessionId}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });
    const data = await res.json();
    append(`🤖 ${data.response}`);
    
    // If a grade is produced, update scoreboard immediately and start a short poll
    if (data?.last_grade) {
      setGrade(data.last_grade);
      // Short-lived poll (e.g., 5 times every 1s) to catch async state persistence
      stopPoll();
      let remaining = 5;
      pollTimer.current = window.setInterval(async () => {
        remaining -= 1;
        await refreshScoreboard(false);
        if (remaining <= 0) stopPoll();
      }, 1000);
    }
  }

  return (
    <div className="container-page space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">EvalForge Dev UI</h1>
          <p className="muted">Quick controls for sessions, grading, and diagnostics.</p>
        </div>
        <ThemeToggle />
      </div>

      {/* Controls */}
      <div className="card p-4">
        <div className="flex flex-wrap gap-2">
          <button className="btn btn-primary" onClick={createSession}>Create Session</button>
          <button className="btn" onClick={() => sendMessage("hi")}>Send "hi"</button>
          <button className="btn" onClick={() => sendMessage("1")}>Select Track "1"</button>
          <button className="btn" onClick={() => sendMessage("function add(a,b){return a+b}")}>Submit Code</button>
          <button
            className="btn"
            onClick={() => refreshScoreboard(true)}
            disabled={!sessionId || loadingGrade}
            data-testid="refresh-scoreboard"
          >
            {loadingGrade ? "Refreshing…" : "Refresh Scoreboard"}
          </button>
        </div>
      </div>

      {/* Scoreboard */}
      <div className="card p-4 space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="section-title">Judge Scoreboard</h2>
          {grade ? (
            <span className="muted">Rubric: coverage · correctness · clarity</span>
          ) : (
            <span className="muted">No grade yet</span>
          )}
        </div>
        <Scoreboard grade={grade} />
        {!grade && <p className="muted">Submit code to Judge to see your rubric scores here.</p>}
      </div>

      {/* Log */}
      <div className="card p-4">
        <h2 className="section-title mb-2">Log</h2>
        <div className="space-y-1 font-mono text-sm text-muted">
          {log.length === 0 ? <div>No events yet.</div> : log.map((l, i) => <div key={i}>{l}</div>)}
        </div>
      </div>
    </div>
  );
}
