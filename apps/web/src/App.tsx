import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { GameShell } from './layouts/GameShell';
import EvalForgeLanding from './pages/EvalForgeLanding';

import { FXLayer } from './components/FXLayer';

function App() {
    return (
        <FXLayer>
            <Routes>
                <Route path="/" element={<EvalForgeLanding />} />
                <Route path="/arcade/*" element={<GameShell />} />
            </Routes>
        </FXLayer>
    );
}

export default App;
