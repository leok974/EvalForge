import React, { useEffect, useRef, useState } from "react";

export const ChatInput: React.FC<{
  disabled?: boolean;
  onSend: (text: string) => Promise<void> | void;
  placeholder?: string;
}> = ({ disabled, onSend, placeholder }) => {
  const [text, setText] = useState("");
  const ref = useRef<HTMLTextAreaElement | null>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const handler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "enter") {
        e.preventDefault();
        if (text.trim().length) {
          Promise.resolve(onSend(text.trim())).then(() => setText(""));
        }
      }
    };
    el.addEventListener("keydown", handler as any);
    return () => el.removeEventListener("keydown", handler as any);
  }, [text, onSend]);

  return (
    <div className="flex items-end gap-2">
      <textarea
        ref={ref}
        className="input w-full min-h-[44px] max-h-[200px] resize-y"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder={placeholder || "Type a message…  (Ctrl/Cmd + Enter to send)"}
        disabled={disabled}
      />
      <button
        className="btn btn-primary"
        disabled={disabled || text.trim().length === 0}
        onClick={async () => {
          const t = text.trim();
          if (!t) return;
          await onSend(t);
          setText("");
        }}
      >
        Send
      </button>
    </div>
  );
};
