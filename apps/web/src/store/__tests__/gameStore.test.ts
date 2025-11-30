import { describe, it, expect, beforeEach } from 'vitest';
import { useGameStore } from '../gameStore';

describe('Game Store', () => {
  beforeEach(() => {
    // Reset store state before each test
    useGameStore.setState({
      xp: 0,
      level: 1,
      layout: 'cyberdeck',
      activeQuestId: null
    });
  });

  it('initializes with defaults', () => {
    const state = useGameStore.getState();
    expect(state.xp).toBe(0);
    expect(state.level).toBe(1);
    expect(state.layout).toBe('cyberdeck');
  });

  it('switches layouts', () => {
    useGameStore.getState().setLayout('navigator');
    expect(useGameStore.getState().layout).toBe('navigator');
  });

  it('calculates levels correctly', () => {
    // 1. Add small XP (No Level Up)
    useGameStore.getState().addXp(500);
    expect(useGameStore.getState().xp).toBe(500);
    expect(useGameStore.getState().level).toBe(1); // floor(500/1000) + 1

    // 2. Add big XP (Level Up)
    useGameStore.getState().addXp(600); // Total 1100
    expect(useGameStore.getState().xp).toBe(1100);
    expect(useGameStore.getState().level).toBe(2); // floor(1100/1000) + 1
  });
});
