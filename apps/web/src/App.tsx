import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { GameShell } from './layouts/GameShell';
import EvalForgeLanding from './pages/EvalForgeLanding';
import DevQA from './pages/DevQA';

import { FXLayer } from './components/FXLayer';

function App() {
    return (
        <FXLayer>
            <Routes>
                <Route path="/" element={<EvalForgeLanding />} />
                <Route path="/arcade/*" element={<GameShell />} />
                <Route path="/dev/qa" element={<DevQA />} />

                {/* Shortcuts */}
                <Route path="/deck" element={<Navigate to="/arcade/deck" replace />} />
                <Route path="/workshop" element={<Navigate to="/arcade/workshop" replace />} />
                <Route path="/orion" element={<Navigate to="/arcade/orion" replace />} />
                <Route path="/worlds/*" element={<Navigate to="/arcade/worlds" replace />} />
            </Routes>
        </FXLayer>
    );
}

export default App;
