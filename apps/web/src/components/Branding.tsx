import React from 'react';

export function NanoLogo() {
    return (
        <div className="flex items-center gap-3 select-none group cursor-pointer">
            {/* 1. Increased size to w-10 h-10 (40px) for clarity 
         2. Removed the inner 'absolute inset-0' overlay that was washing it out
         3. Added 'bg-transparent' instead of black so transparent PNGs look right
      */}
            <div className="relative w-10 h-10 flex items-center justify-center rounded-xl shadow-[0_0_15px_rgba(34,211,238,0.2)] border border-zinc-800 group-hover:border-cyan-500/50 group-hover:scale-105 transition-all overflow-hidden bg-zinc-950">
                <img
                    src="/branding/logo.png"
                    alt="EvalForge Logo"
                    className="w-full h-full object-cover"
                />
            </div>

            {/* Text Logo */}
            <div className="flex flex-col justify-center">
                <span className="font-bold tracking-tighter text-xl leading-none text-white drop-shadow-md">
                    EVAL<span className="text-cyan-400">FORGE</span>
                </span>
                <span className="text-[9px] font-mono text-zinc-500 tracking-[0.2em] uppercase flex items-center gap-1.5 mt-0.5 group-hover:text-cyan-300 transition-colors">
                    <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse shadow-[0_0_5px_#10b981]" />
                    ONLINE
                </span>
            </div>
        </div>
    );
}
