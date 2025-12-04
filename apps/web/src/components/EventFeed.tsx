
import React, { useEffect, useState } from "react";
import {
    QUEST_UNLOCKED_EVENT,
    type QuestUnlockedDetail,
} from "@/lib/questsEvents";

interface EventItem {
    id: string;
    kind: "quest-unlock";
    message: string;
    timestamp: string;
}

export const EventFeed: React.FC = () => {
    const [events, setEvents] = useState<EventItem[]>([]);

    useEffect(() => {
        if (typeof window === "undefined") return;

        const handler = (event: Event) => {
            const custom = event as CustomEvent<QuestUnlockedDetail>;
            const detail = custom.detail;
            if (!detail) return;

            const ts = new Date().toISOString();
            const newEvents: EventItem[] = detail.unlocks.map((u, idx) => {
                const label = u.label ?? u.id;
                const questTitle = detail.quest.title;

                const msg =
                    u.type === "boss"
                        ? `Boss unlocked: ${label} (from quest: ${questTitle})`
                        : `Layout unlocked: ${label} (from quest: ${questTitle})`;

                return {
                    id: `${ts}-${idx}-${u.id}`,
                    kind: "quest-unlock",
                    message: msg,
                    timestamp: ts,
                };
            });

            setEvents((prev) => [...newEvents, ...prev].slice(0, 50));
        };

        window.addEventListener(QUEST_UNLOCKED_EVENT, handler);
        return () => window.removeEventListener(QUEST_UNLOCKED_EVENT, handler);
    }, []);

    if (!events.length) {
        return (
            <div className="text-[11px] text-slate-500">
                No recent events yet.
            </div>
        );
    }

    return (
        <div className="space-y-1.5 text-[10px]" data-testid="event-feed">
            {events.map((ev) => (
                <div
                    key={ev.id}
                    className="flex items-start justify-between gap-2 rounded-md bg-slate-900/80 px-2 py-1"
                >
                    <span className="text-slate-200">{ev.message}</span>
                    <span className="text-[9px] text-slate-500">
                        {new Date(ev.timestamp).toLocaleTimeString()}
                    </span>
                </div>
            ))}
        </div>
    );
};
