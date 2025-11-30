import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { LayoutSwitcher } from '../LayoutSwitcher';
import { useGameStore } from '../../store/gameStore';

describe('LayoutSwitcher', () => {
  it('renders current layout value', () => {
    useGameStore.setState({ layout: 'workshop' });
    render(<LayoutSwitcher />);

    const select = screen.getByRole('combobox') as HTMLSelectElement;
    expect(select.value).toBe('workshop');
  });

  it('updates store on change', () => {
    render(<LayoutSwitcher />);
    const select = screen.getByRole('combobox');

    // Simulate user selecting "Navigator"
    fireEvent.change(select, { target: { value: 'navigator' } });

    expect(useGameStore.getState().layout).toBe('navigator');
  });
});
