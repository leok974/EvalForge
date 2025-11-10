import React, { useRef, useState } from "react";
import { MessageList } from "./MessageList";
import { ChatInput } from "./ChatInput";
import { sendSessionMessageStream } from "../../lib/api";
import { useToast } from "../../lib/toast";

export type Msg = {
  id: string;
  role: "user" | "assistant" | "system";
  text: string;
  ts: number;
};

export const ChatPanel: React.FC<{
  sessionId: string;
  baseUrl?: string;
}> = ({ sessionId, baseUrl }) => {
  const [messages, setMessages] = useState<Msg[]>([]);
  const [busy, setBusy] = useState(false);
  const toast = useToast();
  const abortControllerRef = useRef<AbortController | null>(null);

  const handleSend = async (text: string) => {
    if (!text.trim()) return;

    const userMsg: Msg = {
      id: `user-${Date.now()}`,
      role: "user",
      text: text.trim(),
      ts: Date.now(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setBusy(true);

    // Create abort controller for this stream
    abortControllerRef.current = new AbortController();

    // Create placeholder assistant message
    const assistantId = `assistant-${Date.now()}`;
    const assistantMsg: Msg = {
      id: assistantId,
      role: "assistant",
      text: "",
      ts: Date.now(),
    };
    setMessages((prev) => [...prev, assistantMsg]);

    try {
      await sendSessionMessageStream(
        baseUrl || "",
        sessionId,
        text.trim(),
        {
          onDelta: (token: string) => {
            setMessages((prev) =>
              prev.map((m) =>
                m.id === assistantId ? { ...m, text: m.text + token } : m
              )
            );
          },
          onFinal: (fullText: string) => {
            setMessages((prev) =>
              prev.map((m) =>
                m.id === assistantId ? { ...m, text: fullText } : m
              )
            );
          },
          onError: (error: string) => {
            toast?.push({
              kind: "error",
              title: "Stream error",
              text: error,
            });
          },
        },
        abortControllerRef.current.signal
      );
    } catch (err: any) {
      // Only show error if not aborted
      if (err.name !== "AbortError") {
        toast?.push({
          kind: "error",
          title: "Failed to send message",
          text: err.message || String(err),
        });
      }
    } finally {
      setBusy(false);
      abortControllerRef.current = null;
    }
  };

  const handleStop = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
      setBusy(false);
    }
  };

  return (
    <div className="border border-border rounded-lg p-4 bg-surface flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-text">Chat</h3>
        <div className="flex items-center gap-2">
          {busy && (
            <button className="btn btn-sm" onClick={handleStop}>
              Stop
            </button>
          )}
          <span className="text-xs text-muted">Session: {sessionId}</span>
        </div>
      </div>
      <MessageList items={messages} />
      <ChatInput disabled={busy} onSend={handleSend} />
    </div>
  );
};
