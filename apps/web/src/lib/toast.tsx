import React, { createContext, useContext, useMemo, useRef, useState } from "react";

type ToastKind = "info" | "success" | "error";
export type Toast = { id: string; title?: string; text: string; kind?: ToastKind; ttl?: number };

type Ctx = {
  toasts: Toast[];
  push: (t: Omit<Toast, "id">) => void;
  dismiss: (id: string) => void;
};

const ToastCtx = createContext<Ctx | null>(null);

export const ToastProvider: React.FC<React.PropsWithChildren> = ({ children }) => {
  const [toasts, setToasts] = useState<Toast[]>([]);
  const idSeq = useRef(0);

  const dismiss = (id: string) => setToasts(ts => ts.filter(t => t.id !== id));

  const push: Ctx["push"] = (t) => {
    const id = String(++idSeq.current);
    const toast: Toast = { id, kind: "info", ttl: 3500, ...t };
    setToasts(ts => [toast, ...ts]);
    // auto-remove
    const ttl = Math.max(1000, toast.ttl!);
    setTimeout(() => dismiss(id), ttl);
  };

  const value = useMemo(() => ({ toasts, push, dismiss }), [toasts]);

  return (
    <ToastCtx.Provider value={value}>
      {children}
      {/* Renderer */}
      <div className="pointer-events-none fixed bottom-4 right-4 z-50 flex w-[360px] max-w-[92vw] flex-col gap-2">
        {toasts.map(t => (
          <div
            key={t.id}
            className={[
              "pointer-events-auto rounded-lg border px-4 py-3 shadow-soft animate-in fade-in slide-in-from-bottom-2",
              "bg-surface border-border text-text",
              t.kind === "success" ? "ring-1 ring-success/20" : "",
              t.kind === "error" ? "ring-1 ring-warn/30" : ""
            ].join(" ")}
            role="status"
            aria-live="polite"
          >
            <div className="flex items-start gap-3">
              <div className="text-lg leading-none pt-[1px]">
                {t.kind === "success" ? "✅" : t.kind === "error" ? "⚠️" : "ℹ️"}
              </div>
              <div className="flex-1">
                {t.title ? <div className="font-medium mb-0.5">{t.title}</div> : null}
                <div className="text-sm text-muted">{t.text}</div>
              </div>
              <button
                className="btn btn-ghost -m-2 px-2 py-1"
                onClick={() => dismiss(t.id)}
                aria-label="Dismiss"
              >
                ✕
              </button>
            </div>
          </div>
        ))}
      </div>
    </ToastCtx.Provider>
  );
};

export function useToast() {
  const ctx = useContext(ToastCtx);
  if (!ctx) throw new Error("ToastProvider missing");
  return ctx;
}
