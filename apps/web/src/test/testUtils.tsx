import { ReactNode } from 'react';
import { MemoryRouter } from 'react-router-dom';
import { render } from '@testing-library/react';

/**
 * Renders a component wrapped in MemoryRouter for tests that use react-router hooks
 */
export function renderWithRouter(ui: ReactNode) {
    return render(<MemoryRouter>{ui}</MemoryRouter>);
}
