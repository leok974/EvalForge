import React from 'react';

// Icons (using Lucide React or similar)
// import { Activity, Shield, Zap } from 'lucide-react'; 

export function Scoreboard({ grade }: { grade: any }) {
  if (!grade) {
    return (
      <div className="p-4 border border-zinc-800 rounded-lg bg-zinc-900/50 text-zinc-500 font-mono text-sm text-center">
        WAITING FOR SUBMISSION...
      </div>
    );
  }

  // Dynamic color for score
  const scoreColor = grade.weighted_score > 85 ? 'text-emerald-400' :
    grade.weighted_score > 50 ? 'text-amber-400' : 'text-rose-500';

  const borderColor = grade.weighted_score > 85 ? 'border-emerald-500/30' :
    grade.weighted_score > 50 ? 'border-amber-500/30' : 'border-rose-500/30';

  return (
    <div className={`p-4 rounded-xl bg-zinc-900 border ${borderColor} shadow-lg transition-all duration-500`}>
      <div className="flex justify-between items-start mb-4">
        <div>
          <h2 className="text-xs font-bold text-zinc-400 uppercase tracking-widest">Performance</h2>
          <div className={`text-4xl font-mono font-bold mt-1 ${scoreColor} drop-shadow-md`}>
            {grade.weighted_score}<span className="text-lg opacity-50">%</span>
          </div>
        </div>
        <div className="text-right">
          <div className="text-xs font-mono text-zinc-500">{grade.rubric_used?.toUpperCase() || 'DEFAULT'}</div>
        </div>
      </div>

      {/* Metric Pills */}
      <div className="grid grid-cols-3 gap-2 mb-4">
        <MetricPill label="CVG" val={grade.coverage} max={5} />
        <MetricPill label="COR" val={grade.correctness} max={5} />
        <MetricPill label="CLR" val={grade.clarity} max={5} />
      </div>

      <div className="text-xs font-mono text-zinc-400 border-t border-zinc-800 pt-3 italic">
        "{grade.comment}"
      </div>
    </div>
  );
}

function MetricPill({ label, val, max }: { label: string, val: number, max: number }) {
  return (
    <div className="bg-black/40 rounded p-2 text-center border border-zinc-800">
      <div className="text-[10px] text-zinc-500 mb-1">{label}</div>
      <div className="flex justify-center space-x-0.5">
        {[...Array(max)].map((_, i) => (
          <div key={i} className={`h-1.5 w-1.5 rounded-full ${i < val ? 'bg-cyan-400' : 'bg-zinc-700'}`} />
        ))}
      </div>
    </div>
  );
}
