import React from 'react';
import { GameShell } from './layouts/GameShell';

import { FXLayer } from './components/FXLayer';

function App() {
    return (
        <FXLayer>
            <GameShell />
        </FXLayer>
    );
}

export default App;
