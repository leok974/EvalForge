import { useState, useRef } from 'react';
import { useBossStore } from '../store/bossStore';
import { refreshWorldProgress } from '../features/progress/trackProgress';

type Grade = {
    weighted_score: number;
    coverage: number;
    correctness: number;
    clarity: number;
    comment: string;
    rubric?: string[];
    rubric_used?: string;
};

export type StreamContext = {
    mode: string;
    world_id?: string;
    track_id?: string;
    codex_id?: string;
};

type Message = {
    role: 'user' | 'assistant';
    content: string;
    npc?: {
        name: string;
        title: string;
        avatar_icon: string;
        color: string;
    };
};

export type ProgressUpdate = {
    xp_gained: number;
    world_id: string;
    new_world_level: number;
    world_level_up: boolean;
    new_global_level: number;
    global_level_up: boolean;
};

export function useArcadeStream(sessionId: string, user: string = 'test') {
    const [messages, setMessages] = useState<Message[]>([]);
    const [latestGrade, setLatestGrade] = useState<Grade | null>(null);
    const [lastProgress, setLastProgress] = useState<ProgressUpdate | null>(null);
    const [isStreaming, setIsStreaming] = useState(false);
    const abortControllerRef = useRef<AbortController | null>(null);

    const sendMessage = async (text: string, mode: string = 'judge', worldId?: string, trackId?: string, codexId?: string) => {
        // 1. Setup UI State
        setIsStreaming(true);
        setMessages(prev => [...prev, { role: 'user', content: text }]);
        // Add placeholder for assistant response
        setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

        abortControllerRef.current = new AbortController();

        try {
            const response = await fetch(
                `/apps/arcade_app/users/${user}/sessions/${sessionId}/query/stream`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'text/event-stream',
                    },
                    body: JSON.stringify({
                        message: text,
                        mode,
                        world_id: worldId,
                        track_id: trackId,
                        codex_id: codexId
                    }),
                    signal: abortControllerRef.current.signal,
                }
            );

            if (!response.ok) throw new Error(`Network response was not ok: ${response.status}`);

            // 2. Read the Stream
            const reader = response.body?.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            if (!reader) return;

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                buffer += chunk;

                // Split by double newline (SSE standard delimiter)
                // Handle both \n\n and \r\n\r\n
                const parts = buffer.split(/\n\n|\r\n\r\n/);
                buffer = parts.pop() || ''; // Keep the last incomplete chunk in buffer

                for (const part of parts) {
                    if (part.trim()) {
                        parseEvent(part);
                    }
                }
            }

        } catch (error: any) {
            if (error.name !== 'AbortError') {
                console.error('Stream error:', error);
                setMessages(prev => {
                    const newHistory = [...prev];
                    const lastMsg = newHistory[newHistory.length - 1];
                    if (lastMsg.role === 'assistant') {
                        lastMsg.content += `\n[Error: ${error.message}]`;
                    }
                    return newHistory;
                });
            }
        } finally {
            setIsStreaming(false);
            abortControllerRef.current = null;
        }
    };

    const parseEvent = (textChunk: string) => {
        // Normalize newlines to \n
        const cleanChunk = textChunk.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
        const lines = cleanChunk.split('\n');

        let eventType = 'message';
        let data = '';

        for (const line of lines) {
            if (line.startsWith('event: ')) {
                eventType = line.slice(7).trim();
            }
            else if (line.startsWith('data: ')) {
                const lineData = line.slice(6);
                // If data already has content, append with newline (spec behavior)
                data = data ? data + '\n' + lineData : lineData;
            }
        }

        if (!data || data === '[DONE]') return;

        if (eventType === 'grade') {
            try {
                const gradeData = JSON.parse(data);
                setLatestGrade(gradeData);
            } catch (e) { console.error('Failed to parse grade', e); }
        }
        else if (eventType === 'progress') {
            try {
                const p = JSON.parse(data);
                setLastProgress(p);
            } catch (e) { console.error(e); }
        }
        else if (eventType === 'text_delta') {
            setMessages(prev => {
                const newHistory = [...prev];
                const lastMsg = newHistory[newHistory.length - 1];
                if (lastMsg.role === 'assistant') {
                    lastMsg.content += data;
                }
                return newHistory;
            });
        }
        else if (eventType === 'npc_identity') {
            try {
                const npcData = JSON.parse(data);
                setMessages(prev => {
                    const newHistory = [...prev];
                    const lastMsg = newHistory[newHistory.length - 1];
                    if (lastMsg.role === 'assistant') {
                        lastMsg.npc = npcData;
                    }
                    return newHistory;
                });
            } catch (e) { console.error('Failed to parse npc_identity', e); }
        }
        else if (eventType === 'boss_result') {
            try {
                const resultData = JSON.parse(data);
                useBossStore.getState().applyBossResult(resultData);

                // If boss was defeated, refresh world progress (Orion + Practice Gauntlet)
                if (resultData.passed) {
                    refreshWorldProgress().catch(err =>
                        console.warn('World progress refresh failed after boss completion', err)
                    );
                }
            } catch (e) { console.error('Failed to parse boss_result', e); }
        }
    };

    const stopStream = () => {
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
            setIsStreaming(false);
        }
    };

    return { messages, setMessages, latestGrade, lastProgress, isStreaming, sendMessage, stopStream };
}
