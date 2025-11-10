import React, { useEffect, useRef } from "react";
import { Msg, MessageBubble } from "./MessageBubble";

export const MessageList: React.FC<{ items: Msg[] }> = ({ items }) => {
  const endRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => { endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" }); }, [items]);
  return (
    <div className="h-[380px] overflow-auto pr-1">
      {items.length === 0 ? (
        <div className="muted">No messages yet. Create a session, then start chatting.</div>
      ) : (
        items.map(m => <MessageBubble key={m.id} m={m} />)
      )}
      <div ref={endRef} />
    </div>
  );
};
