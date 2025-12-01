import { useState, useEffect } from 'react';

export type User = {
    id: string;
    name: string;
    avatar_url: string;
    auth_mode: string;
    current_avatar_id?: string;
    avatar?: any; // In a real app, import AvatarDef
};

export function useAuth() {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    const checkAuth = async () => {
        try {
            const res = await fetch('/api/auth/me');
            if (res.ok) {
                const data = await res.json();
                // API returns empty object {} if not logged in
                if (data && data.id) {
                    setUser(data);
                } else {
                    setUser(null);
                }
            }
        } catch (err) {
            console.error("Auth check failed", err);
        } finally {
            setLoading(false);
        }
    };

    const login = () => {
        fetch('/api/auth/github/start')
            .then(r => r.json())
            .then(data => {
                // Force browser to navigate to GitHub (or the mock callback)
                window.location.href = data.url;
            });
    };

    const logout = () => {
        // For mock, just clear local state. 
        // In a real app, you'd hit a /logout endpoint to clear cookies.
        setUser(null);
    };

    useEffect(() => {
        checkAuth();
    }, []);

    return { user, loading, login, logout, refresh: checkAuth };
}
