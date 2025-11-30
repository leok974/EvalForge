import { useState, useEffect } from 'react';

export type User = {
    id: string;
    name: string;
    avatar_url: string;
    auth_mode: string;
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
        // In mock mode, we trigger the 'start' endpoint which sets up the state, 
        // then immediately re-check /me to get the user object.
        fetch('/api/auth/github/start')
            .then(() => checkAuth());
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
