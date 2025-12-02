import { useState, useEffect, useCallback } from 'react';

export type SkillNode = {
    id: string;
    name: string;
    description: string;
    cost: number;
    tier: number;
    category: string;
    feature_key: string;
    parent_id: string | null;
    is_unlocked: boolean;
    can_unlock: boolean;
};

export function useSkills(user: any) {
    const [skills, setSkills] = useState<SkillNode[]>([]);
    const [skillPoints, setSkillPoints] = useState(0);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Fetch Tree
    const refreshSkills = useCallback(() => {
        if (!user) return;
        setLoading(true);
        setError(null);
        fetch('/api/skills')
            .then(r => {
                if (!r.ok) throw new Error(`HTTP ${r.status}`);
                return r.json();
            })
            .then(data => {
                setSkills(data.nodes || []);
                setSkillPoints(data.skill_points || 0);
                setLoading(false);
            })
            .catch(e => {
                console.error("Failed to fetch skills", e);
                setError("Failed to load skill tree");
                setLoading(false);
            });
    }, [user]);

    // Initial Load
    useEffect(() => {
        refreshSkills();
    }, [refreshSkills]);

    // Unlock Action
    const unlockSkill = async (skillId: string) => {
        try {
            const res = await fetch('/api/skills/unlock', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ skill_id: skillId })
            });

            const data = await res.json();

            if (res.ok) {
                refreshSkills(); // Reload state to update dependency graph
                return { success: true };
            } else {
                return { success: false, error: data.detail || "Failed to unlock" };
            }
        } catch (e) {
            return { success: false, error: "Network Error" };
        }
    };

    // Helper for UI Gating
    const hasSkill = (featureKey: string) => {
        // If not loaded yet, assume false (secure by default)
        const skill = skills.find(s => s.feature_key === featureKey);
        return skill ? skill.is_unlocked : false;
    };

    return { skills, skillPoints, unlockSkill, hasSkill, refreshSkills, loading, error };
}
