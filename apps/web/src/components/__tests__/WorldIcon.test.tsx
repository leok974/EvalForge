import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import { WorldIcon } from '../WorldIcon';
import React from 'react';

// Mock Lucide React to inspect which icon is actually rendered
// We replace the icons with dummy components that have test-ids
vi.mock('lucide-react', () => ({
    Factory: (props: any) => <svg data-testid="icon-factory" {...props} />,
    Box: (props: any) => <svg data-testid="icon-box" {...props} />,
    Aperture: (props: any) => <svg data-testid="icon-aperture" {...props} />,
    HelpCircle: (props: any) => <svg data-testid="icon-help-circle" {...props} />,
    Sun: (props: any) => <svg data-testid="icon-sun" {...props} />,
    Gem: (props: any) => <svg data-testid="icon-gem" {...props} />,
    Database: (props: any) => <svg data-testid="icon-database" {...props} />,
    Server: (props: any) => <svg data-testid="icon-server" {...props} />,
    Bot: (props: any) => <svg data-testid="icon-bot" {...props} />,
    GitBranch: (props: any) => <svg data-testid="icon-git-branch" {...props} />,
    Brain: (props: any) => <svg data-testid="icon-brain" {...props} />
}));

describe('WorldIcon Component', () => {
    it('renders correct icon for known key', () => {
        const { getByTestId } = render(<WorldIcon iconName="factory" />);
        expect(getByTestId('icon-factory')).toBeDefined();
    });

    it('renders fallback icon for unknown key', () => {
        const { getByTestId } = render(<WorldIcon iconName="unknown_random_string" />);
        // Should default to HelpCircle based on WorldIcon.tsx implementation
        expect(getByTestId('icon-help-circle')).toBeDefined();
    });

    it('renders specific system icon', () => {
        const { getByTestId } = render(<WorldIcon iconName="aperture" />);
        expect(getByTestId('icon-aperture')).toBeDefined();
    });

    it('passes className prop correctly', () => {
        const { getByTestId } = render(<WorldIcon iconName="factory" className="text-red-500" />);
        const icon = getByTestId('icon-factory');
        expect(icon.getAttribute('class')).toContain('text-red-500');
    });
});
