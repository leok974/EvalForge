import { render, screen, fireEvent } from '@testing-library/react';
import { OrionMap } from '../OrionMap';
import { vi, test, expect } from 'vitest';
import { useNavigate } from 'react-router-dom';

// Mock useNavigate
vi.mock('react-router-dom', async (importOriginal) => {
    const actual = await importOriginal<{}>();
    return {
        ...actual,
        useNavigate: vi.fn(),
    };
});

test('clicking The Reactor focuses world-java', () => {
    // Setup
    const navigate = vi.fn();
    (useNavigate as any).mockReturnValue(navigate);

    render(<OrionMap />);

    // Act
    const reactorBtn = screen.getByTestId('orion-world-java');
    fireEvent.click(reactorBtn);

    // Assert
    expect(navigate).toHaveBeenCalledWith('/worlds/world-java');
});
