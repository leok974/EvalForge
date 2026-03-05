import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { QueryInspector } from '../QueryInspector';
import { useQuestStore } from '@/store/questStore';

// Mock the zustand store
vi.mock('@/store/questStore', () => ({
    useQuestStore: vi.fn(),
}));

describe('QueryInspector', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('renders empty state when no artifacts exist', () => {
        (useQuestStore as any).mockImplementation((selector: any) => selector({ lastRunResult: null }));
        render(<QueryInspector />);
        expect(screen.getByText('Query Inspector')).toBeInTheDocument();
        expect(screen.getByText('Run a SQL task to capture execution traces.')).toBeInTheDocument();
    });

    it('renders trace list grouped by phase (setup collapsed)', () => {
        const mockResult = {
            artifacts: {
                sql_trace: [
                    { phase: 'setup', elapsed_ms: 10, sql: 'CREATE TABLE t (id INT);', error: null, row_count: null },
                    { phase: 'setup', elapsed_ms: 5, sql: 'INSERT INTO t VALUES (1);', error: null, row_count: null },
                    { phase: 'student', elapsed_ms: 20, sql: 'SELECT * FROM t;', error: null, row_count: 1 },
                ]
            }
        };
        (useQuestStore as any).mockImplementation((selector: any) => selector({ lastRunResult: mockResult }));

        render(<QueryInspector />);

        // Tab is trace by default
        expect(screen.getByText(/Setup Phase \(2 queries\)/)).toBeInTheDocument();

        // Setup details should be hidden by default
        expect(screen.queryByText('CREATE TABLE t (id INT);')).not.toBeInTheDocument();

        // Student SQL should be visible (expanded by default)
        expect(screen.getAllByText('SELECT * FROM t;').length).toBeGreaterThan(0);

        // Expand setup
        fireEvent.click(screen.getByText(/Setup Phase \(2 queries\)/));
        expect(screen.getAllByText('CREATE TABLE t (id INT);').length).toBeGreaterThan(0);
    });

    it('pin failing statement (force expands automatically)', () => {
        const mockResult = {
            artifacts: {
                sql_trace: [
                    { phase: 'student', elapsed_ms: 1, sql: 'SELECT * FRO t;', error: 'Syntax error near FRO', row_count: null },
                ]
            }
        };
        (useQuestStore as any).mockImplementation((selector: any) => selector({ lastRunResult: mockResult }));

        render(<QueryInspector />);

        // Should be expanded automatically and show the error text
        expect(screen.getByText('Syntax error near FRO')).toBeInTheDocument();
    });

    it('renders result tab table headers and rows', () => {
        const mockResult = {
            artifacts: {
                sql_trace: [],
                sql_student_result: {
                    columns: ['id', 'name'],
                    preview_rows: [[1, 'Alice'], [2, 'Bob']]
                }
            }
        };
        (useQuestStore as any).mockImplementation((selector: any) => selector({ lastRunResult: mockResult }));

        render(<QueryInspector />);

        fireEvent.click(screen.getByText('Result'));

        expect(screen.getByText('id')).toBeInTheDocument();
        expect(screen.getByText('name')).toBeInTheDocument();
        expect(screen.getByText('Alice')).toBeInTheDocument();
        expect(screen.getByText('Bob')).toBeInTheDocument();
    });

    it('renders explain tab plan rows', () => {
        const mockResult = {
            artifacts: {
                sql_trace: [],
                sql_explain: {
                    engine: 'sqlite',
                    statement: 'SELECT 1;',
                    plan_rows: ['SCAN TABLE t']
                }
            }
        };
        (useQuestStore as any).mockImplementation((selector: any) => selector({ lastRunResult: mockResult }));

        render(<QueryInspector />);

        fireEvent.click(screen.getByText('Explain'));

        expect(screen.getByText('Statement Analyzed (sqlite)')).toBeInTheDocument();
        expect(screen.getByText('SELECT 1;')).toBeInTheDocument();
        expect(screen.getByText('SCAN t')).toBeInTheDocument(); // because we replace SCAN TABLE with SCAN inside the component
    });
});
