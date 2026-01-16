import React, { useRef, useImperativeHandle, forwardRef, useEffect, useState } from 'react';
import Editor, { OnMount } from '@monaco-editor/react';
import { Loader2, Zap } from 'lucide-react';

export interface QuestEditorRef {
    jumpToLine: (line: number) => void;
}

interface QuestEditorProps {
    language?: string;
    value: string;
    onChange: (v: string) => void;
    isSaving?: boolean;
    readOnly?: boolean;
}

export const QuestEditor = forwardRef<QuestEditorRef, QuestEditorProps>(({
    language = "python",
    value,
    onChange,
    isSaving = false,
    readOnly = false,
}, ref) => {
    const editorRef = useRef<any>(null);
    const decorationsRef = useRef<string[]>([]);

    // Toggle for "Optical Enhancer" (Stub)
    const [enhancedMode, setEnhancedMode] = useState(true);

    const handleEditorDidMount: OnMount = (editor, monaco) => {
        editorRef.current = editor;
    };

    useImperativeHandle(ref, () => ({
        jumpToLine: (lineNumber: number) => {
            const editor = editorRef.current;
            if (!editor) return;

            editor.revealLineInCenter(lineNumber);
            editor.setPosition({ column: 1, lineNumber });
            editor.focus();

            // Flash highlight
            // (In a real implementation, we'd use monaco.editor.deltaDecorations)
            // For now, we rely on selection highlight
        }
    }));

    return (
        <div className="h-full flex flex-col relative rounded-xl border border-white/10 bg-zinc-950 overflow-hidden shadow-inner group">
            {/* Optical Enhancer Toggle (Stub) */}
            <div className="absolute top-2 right-4 z-10 flex items-center gap-2 pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity">
                {isSaving && <span className="text-[10px] text-zinc-500 flex items-center gap-1"><Loader2 className="w-3 h-3 animate-spin" /> Saving</span>}
                <div className="pointer-events-auto">
                    <button
                        onClick={() => setEnhancedMode(!enhancedMode)}
                        title="Toggle Optical Enhancer"
                        className={`p-1 rounded ${enhancedMode ? 'bg-cyan-950/50 text-cyan-400' : 'bg-zinc-900 text-zinc-600'}`}
                    >
                        <Zap className="w-3 h-3" />
                    </button>
                </div>
            </div>

            <div className="flex-1 min-h-0">
                <Editor
                    height="100%"
                    defaultLanguage={language}
                    value={value}
                    onChange={(v) => onChange(v ?? "")}
                    onMount={handleEditorDidMount}
                    theme="vs-dark"
                    options={{
                        fontSize: 14,
                        minimap: { enabled: false },
                        scrollBeyondLastLine: false,
                        wordWrap: "on",
                        lineNumbers: "on",
                        renderLineHighlight: "all",
                        smoothScrolling: true,
                        padding: { top: 14, bottom: 14 },
                        fontFamily: 'JetBrains Mono, Menlo, monospace',
                        // "Enhancer" features toggled via options could go here
                        guides: { indentation: enhancedMode },
                        folding: enhancedMode,
                        readOnly: readOnly,
                    }}
                />
            </div>
        </div>
    );
});

QuestEditor.displayName = 'QuestEditor';
