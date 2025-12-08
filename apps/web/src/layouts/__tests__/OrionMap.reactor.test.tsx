import { render, screen, fireEvent } from '@testing-library/react';
import { OrionMap } from '../OrionMap';
import { vi, test, expect } from 'vitest';
import { useNavigate } from 'react-router-dom';

// Mock useNavigate
vi.mock('react-router-dom', async (importOriginal) => {
    const actual = await importOriginal();
    // @ts-ignore
    return {
        ...actual,
        useNavigate: vi.fn(),
    };
});

test('clicking The Reactor focuses world-java', () => {
    // Setup
    const navigate = vi.fn();
    (useNavigate as any).mockReturnValue(navigate);

    // Render (Mocking GameStore via global mock if needed, but Map might use local state or props.
    // Assuming OrionMap uses useGameStore, which we mocked in testUtils or globally)

    import { render, screen, fireEvent } from '@testing-library/react';
    import { OrionMap } from '../OrionMap';
    import { vi, test, expect } from 'vitest';
    import { useNavigate } from 'react-router-dom';

    // Mock useNavigate
    vi.mock('react-router-dom', async (importOriginal) => {
        const actual = await importOriginal();
        // @ts-ignore
        return {
            ...actual,
            useNavigate: vi.fn(),
        };
    });

    test('clicking The Reactor focuses world-java', () => {
        // Setup
        const navigate = vi.fn();
        (useNavigate as any).mockReturnValue(navigate);

        // Render (Mocking GameStore via global mock if needed, but Map might use local state or props.
        // Assuming OrionMap uses useGameStore, which we mocked in testUtils or globally)

        // Note: Depending on implementation, OrionMap might need a wrapping provider. 
        // But based on previous tests, it seems standalone-ish or assumes store is mocked.

        render(<OrionMap />);

        // Act
        const reactorBtn = screen.getByTestId('orion-world-java');
        fireEvent.click(reactorBtn);

        // Assert
        expect(navigate).toHaveBeenCalledWith('/worlds/world-java');
    });
