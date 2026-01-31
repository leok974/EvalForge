import React from 'react';
import { Routes, Route, Navigate } from "react-router-dom";
import { FXLayer } from "./components/FXLayer";
import { GameShell } from "./layouts/GameShell";
import EvalForgeLanding from "./pages/EvalForgeLanding";
import DevQA from "./pages/DevQA";

// Dev mode check: Only show /dev/qa in development builds
const isDev = import.meta.env.DEV || import.meta.env.VITE_DEV_MODE === 'true';

function App() {
    return (
        <FXLayer>
            <Routes>
                <Route path="/" element={<EvalForgeLanding />} />
                <Route path="/arcade/*" element={<GameShell />} />

                {/* Dev-only routes (hidden in production) */}
                {isDev && <Route path="/dev/qa" element={<DevQA />} />}

                {/* Shortcuts */}
                <Route path="/deck" element={<Navigate to="/arcade/deck" replace />} />
                <Route path="/day" element={<Navigate to="/arcade/day" replace />} />
                <Route path="/workshop" element={<Navigate to="/arcade/workshop" replace />} />
            </Routes>
        </FXLayer>
    );
}

export default App;
