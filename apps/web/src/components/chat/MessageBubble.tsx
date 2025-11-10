import React from "react";

export type Msg = { id: string; role: "user" | "assistant" | "system"; text: string; ts?: number };

export const MessageBubble: React.FC<{ m: Msg }> = ({ m }) => {
  const isUser = m.role === "user";
  const isAssistant = m.role === "assistant";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} my-1`}>
      <div
        className={[
          "max-w-[80%] rounded-lg border",
          isUser ? "bg-brand text-brandFg border-transparent" : "bg-surface text-text border-border",
          "px-3 py-2 whitespace-pre-wrap"
        ].join(" ")}
        data-role={m.role}
      >
        {isAssistant ? (
          <span style={{ whiteSpace: "pre-wrap" }}>{m.text}</span>
        ) : (
          <span>{m.text}</span>
        )}
      </div>
    </div>
  );
};
