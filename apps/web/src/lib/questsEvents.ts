
import type { QuestSummary, QuestUnlockEvent } from "./questsApi";

export const QUEST_UPDATED_EVENT = "evalforge:quest:updated";
export const QUEST_UNLOCKED_EVENT = "evalforge:quest:unlocked";

export interface QuestUpdatedDetail {
    quest: QuestSummary;
}

export interface QuestUnlockedDetail {
    quest: QuestSummary;
    unlocks: QuestUnlockEvent[];
}

export function broadcastQuestUpdate(quest: QuestSummary) {
    if (typeof window === "undefined") return;
    window.dispatchEvent(
        new CustomEvent<QuestUpdatedDetail>(QUEST_UPDATED_EVENT, {
            detail: { quest },
        })
    );
}

export function broadcastQuestUnlocks(
    quest: QuestSummary,
    unlocks: QuestUnlockEvent[]
) {
    if (typeof window === "undefined") return;
    if (!unlocks.length) return;

    window.dispatchEvent(
        new CustomEvent<QuestUnlockedDetail>(QUEST_UNLOCKED_EVENT, {
            detail: { quest, unlocks },
        })
    );
}
