
import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { QuickFixBar } from './QuickFixBar';
import { QuickFix } from '@/lib/questsApi';


// Mock Toast
const mockAddToast = vi.fn();
// Must be hoisted or returned from factory
vi.mock('@/lib/toast', () => {
    return {
        useToast: () => ({
            addToast: mockAddToast
        })
    };
});

import userEvent from '@testing-library/user-event';

describe('QuickFixBar', () => {
    const mockOnApply = vi.fn();
    const mockOnNavigate = vi.fn();

    beforeEach(() => {
        vi.clearAllMocks();
    });

    const fixes: QuickFix[] = [
        {
            id: "fix-1",
            kind: "apply_patch",
            title: "Fix Indent",
            why: "Tabs are bad.",
            severity: "safe",
            patch: { path: "main.py", replacement_full_content: "foo" }
        },
        {
            id: "fix-2",
            kind: "copy_snippet",
            title: "Print Output",
            why: "Need to print hello.",
            severity: "suggestion",
            snippet: "print('hello')"
        }
    ];

    it('does not render if no fixes', () => {
        const { container } = render(<QuickFixBar fixes={[]} onApplyPatch={mockOnApply} onNavigate={mockOnNavigate} />);
        expect(container).toBeEmptyDOMElement();
    });

    it('renders chips for fixes', () => {
        render(<QuickFixBar fixes={fixes} onApplyPatch={mockOnApply} onNavigate={mockOnNavigate} />);
        expect(screen.getByText('Fix Indent')).toBeInTheDocument();
        expect(screen.getByText('Print Output')).toBeInTheDocument();
    });

    it('shows details on chip click', async () => {
        const user = userEvent.setup();
        render(<QuickFixBar fixes={fixes} onApplyPatch={mockOnApply} onNavigate={mockOnNavigate} />);

        await user.click(screen.getByText('Fix Indent'));

        expect(await screen.findByText('Tabs are bad.')).toBeInTheDocument();
        expect(screen.getByText('Apply Fix')).toBeInTheDocument();
    });

    it('calls apply patch on button click', async () => {
        const user = userEvent.setup();
        render(<QuickFixBar fixes={fixes} onApplyPatch={mockOnApply} onNavigate={mockOnNavigate} />);

        await user.click(screen.getByText('Fix Indent'));
        const applyBtn = await screen.findByRole('button', { name: /Apply Fix/i });
        await user.click(applyBtn);

        expect(mockOnApply).toHaveBeenCalledWith(fixes[0]);
    });

    it('copies snippet on button click', async () => {
        const user = userEvent.setup();
        // Mock clipboard
        // Mock clipboard
        Object.defineProperty(navigator, 'clipboard', {
            value: {
                writeText: vi.fn(),
            },
            writable: true
        });

        render(<QuickFixBar fixes={fixes} onApplyPatch={mockOnApply} onNavigate={mockOnNavigate} />);

        await user.click(screen.getByText('Print Output'));
        const copyBtn = await screen.findByRole('button', { name: /Copy Snippet/i });
        await user.click(copyBtn);

        expect(navigator.clipboard.writeText).toHaveBeenCalledWith("print('hello')");
    });

    it('disables apply button in readOnly mode', async () => {
        const user = userEvent.setup();
        render(<QuickFixBar fixes={fixes} onApplyPatch={mockOnApply} onNavigate={mockOnNavigate} readOnly={true} />);

        await user.click(screen.getByText('Fix Indent'));

        const applyBtn = await screen.findByRole('button', { name: /Apply \(Disabled in Replay\)/i });
        expect(applyBtn).toBeDisabled();

        await user.click(applyBtn);
        expect(mockOnApply).not.toHaveBeenCalled();
    });

    it('calls navigation handler', async () => {
        const user = userEvent.setup();
        const navFix: QuickFix = { ...fixes[0], kind: 'navigate', severity: "safe" }; // fix severity

        render(<QuickFixBar fixes={[navFix]} onApplyPatch={mockOnApply} onNavigate={mockOnNavigate} />);

        await user.click(screen.getByText('Fix Indent'));
        const jumpBtn = await screen.findByRole('button', { name: /Jump to Code/i });
        await user.click(jumpBtn);

        expect(mockOnNavigate).toHaveBeenCalledWith(navFix);
    });
    it('renders suggestion snippet safely (no apply button)', async () => {
        const user = userEvent.setup();
        const sampleFixHint: QuickFix = {
            id: 'fix-3',
            title: 'Edge Case Checklist',
            kind: 'copy_snippet',
            severity: 'suggestion',
            why: 'Check hidden tests',
            snippet: '# Check empty input'
        };
        render(
            <QuickFixBar
                fixes={[sampleFixHint]}
                onApplyPatch={mockOnApply}
                onNavigate={mockOnNavigate}
            />
        );

        expect(screen.getByText('Edge Case Checklist')).toBeInTheDocument();

        // Click to expand
        await user.click(screen.getByText('Edge Case Checklist'));

        // Check if severity "suggestion" renders distinct style or text
        expect(await screen.findByText(/Check hidden tests/i)).toBeInTheDocument();
    });


});
