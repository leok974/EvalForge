import React from 'react';
import { useSettingsStore } from '../store/settingsStore';
import { useGameStore } from '../store/gameStore';
import { Volume2, Monitor, Zap, Activity } from 'lucide-react';

interface Props {
    isOpen: boolean;
    onClose: () => void;
}

export function SettingsModal({ isOpen, onClose }: Props) {
    const settings = useSettingsStore();
    const { layout } = useGameStore();

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-[60] flex items-center justify-center p-4"> {/* Z-60 ensures it's above FX layers */}
            <div className="bg-nano-900 border border-zinc-800 rounded-xl w-full max-w-md shadow-2xl overflow-hidden">

                {/* Header */}
                <div className="p-4 border-b border-zinc-800 flex justify-between items-center bg-zinc-900/50">
                    <h2 className="text-white font-bold tracking-wider font-mono flex items-center gap-2">
                        <span className="text-xl">⚙️</span> SYSTEM CONFIG
                    </h2>
                    <button onClick={onClose} className="text-zinc-500 hover:text-white transition-colors">✕</button>
                </div>

                {/* Body */}
                <div className="p-6 space-y-8">

                    {/* Audio Section */}
                    <section>
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="text-xs font-bold text-zinc-500 uppercase tracking-widest flex items-center gap-2">
                                <Volume2 className="w-4 h-4" /> Audio Matrix
                            </h3>
                            <button onClick={settings.toggleMute} className={`text-[10px] px-2 py-1 rounded border ${settings.muted ? 'bg-red-900/20 text-red-400 border-red-900' : 'bg-zinc-800 text-zinc-400 border-zinc-700'}`}>
                                {settings.muted ? 'MUTED' : 'ACTIVE'}
                            </button>
                        </div>
                        <div className="space-y-4">
                            <VolumeSlider label="Master" value={settings.masterVolume} onChange={(v) => settings.setVolume('master', v)} />
                            <VolumeSlider label="UI" value={settings.uiVolume} onChange={(v) => settings.setVolume('ui', v)} />
                            <VolumeSlider label="SFX" value={settings.sfxVolume} onChange={(v) => settings.setVolume('sfx', v)} />
                        </div>
                    </section>

                    <div className="h-px bg-zinc-800" />

                    {/* Visual Section */}
                    <section>
                        <h3 className="text-xs font-bold text-zinc-500 uppercase tracking-widest flex items-center gap-2 mb-4">
                            <Monitor className="w-4 h-4" /> Visual FX
                        </h3>

                        <div className="grid grid-cols-1 gap-2">
                            {layout === 'cyberdeck' && (
                                <Toggle
                                    label="CRT Simulation"
                                    desc="Scanlines and chromatic aberration."
                                    active={settings.crtMode}
                                    onClick={() => settings.toggleVisual('crtMode')}
                                    icon={Monitor}
                                />
                            )}

                            <Toggle
                                label="Haptic Shake"
                                desc="Screen vibration on critical events."
                                active={settings.screenShake}
                                onClick={() => settings.toggleVisual('screenShake')}
                                icon={Activity}
                            />
                            <Toggle
                                label="Particle Emitters"
                                desc="Confetti on success states."
                                active={settings.particles}
                                onClick={() => settings.toggleVisual('particles')}
                                icon={Zap}
                            />
                        </div>
                    </section>

                </div>
            </div>
        </div>
    );
}

// Sub-components for cleanliness
function VolumeSlider({ label, value, onChange }: { label: string, value: number, onChange: (v: number) => void }) {
    return (
        <div className="flex items-center gap-4">
            <span className="text-xs text-zinc-400 w-24 font-mono">{label}</span>
            <input
                type="range" min="0" max="1" step="0.1"
                value={value}
                onChange={(e) => onChange(parseFloat(e.target.value))}
                className="flex-1 accent-cyan-400 h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer"
            />
            <span className="text-xs text-zinc-600 w-8 text-right">{(value * 100).toFixed(0)}%</span>
        </div>
    );
}

function Toggle({ label, desc, active, onClick, icon: Icon }: any) {
    return (
        <button
            onClick={onClick}
            className={`flex items-center justify-between p-3 rounded-lg border transition-all ${active ? 'bg-cyan-950/20 border-cyan-500/50' : 'bg-zinc-900 border-zinc-800 opacity-60 hover:opacity-100'}`}
        >
            <div className="flex items-center gap-3 text-left">
                <div className={`p-2 rounded ${active ? 'bg-cyan-900 text-cyan-400' : 'bg-zinc-800 text-zinc-500'}`}>
                    <Icon className="w-4 h-4" />
                </div>
                <div>
                    <div className={`text-sm font-bold ${active ? 'text-white' : 'text-zinc-400'}`}>{label}</div>
                    <div className="text-[10px] text-zinc-500">{desc}</div>
                </div>
            </div>
            <div className={`w-3 h-3 rounded-full ${active ? 'bg-cyan-400 shadow-[0_0_10px_#22d3ee]' : 'bg-zinc-700'}`} />
        </button>
    );
}
