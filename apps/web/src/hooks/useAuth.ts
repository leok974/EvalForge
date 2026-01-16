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
        // 🔧 Dev-mode bypass: detect localhost at runtime
        // Can be disabled by setting VITE_DEV_FAKE_AUTH=0 in .env.local
        const isLocalDev = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
        const fakeAuthEnabled = import.meta.env.VITE_DEV_FAKE_AUTH !== '0';

        if (isLocalDev && fakeAuthEnabled) {
            console.log('[useAuth] DEV mode (localhost) – using fake user, no /api/auth/me call');
            setUser({
                id: 'dev-user',
                name: 'EvalForge Dev',
                avatar_url: 'https://www.gravatar.com/avatar?d=identicon',
                auth_mode: 'dev',
            });
            setLoading(false);
            return;
        }

        console.log('[useAuth] Real auth mode - calling /api/auth/me');
        // 🔧 Production auth flow
        try {
            // Timeout after 5 seconds to prevent infinite hanging
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000);

            console.log("Checking auth...");
            try {
                const res = await fetch('/api/auth/me', {
                    credentials: 'include',
                    signal: controller.signal
                });
                clearTimeout(timeoutId);

                console.log("Auth status:", res.status);
                if (res.ok) {
                    const data = await res.json();
                    if (data && data.id) {
                        setUser(data);
                    } else {
                        setUser(null);
                    }
                } else if (res.status === 401) {
                    // Not logged in - that's fine, anonymous mode
                    setUser(null);
                }
            } catch (fetchErr: any) {
                if (fetchErr.name === 'AbortError') {
                    console.warn("Auth check timed out - defaulting to guest/offline");
                } else {
                    console.error("Auth check failed", fetchErr);
                }
                setUser(null);
            } finally {
                setLoading(false);
            }
        } catch (error) {
            console.error('Auth error:', error);
            setUser(null);
            setLoading(false);
        }
    };

    const login = () => {
        fetch('/api/auth/login')
            .then(r => r.json())
            .then(data => {
                if (data.url) {
                    window.location.href = data.url;
                } else {
                    console.error("Login failed: No URL returned", data);
                }
            })
            .catch(err => {
                console.error("Login error:", err);
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
