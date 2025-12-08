// src/boss/typeGuardian/auth.ts

export type Credentials = {
    email: string;
    password: string;
};

export interface User {
    id: string;
    email: string;
    name: string;
    role: 'user' | 'admin';
}

export interface Session {
    token: string;
    user: User;
    issuedAt: string;  // ISO timestamp
    expiresAt: string; // ISO timestamp
}

export type AuthErrorKind =
    | 'invalid_credentials'
    | 'locked_out'
    | 'network_error';

export type AuthSuccess = {
    kind: 'success';
    session: Session;
};

export type AuthFailure = {
    kind: 'failure';
    reason: AuthErrorKind;
    message: string;
};

export type AuthResult = AuthSuccess | AuthFailure;

export function isAuthSuccess(result: AuthResult): result is AuthSuccess {
    return result.kind === 'success';
}

export function isAuthFailure(result: AuthResult): result is AuthFailure {
    return result.kind === 'failure';
}

export async function authenticate(
    credentials: Credentials
): Promise<AuthResult> {
    // In the boss scenario this could call a stubbed backend;
    // here we just simulate a couple of paths.

    if (!credentials.email || !credentials.password) {
        return {
            kind: 'failure',
            reason: 'invalid_credentials',
            message: 'Email and password are required.'
        };
    }

    // Simulate a real user
    if (credentials.email === 'admin@example.com' &&
        credentials.password === 'password123') {
        const now = new Date();
        const expires = new Date(now.getTime() + 60 * 60 * 1000);

        const user: User = {
            id: 'admin-1',
            email: credentials.email,
            name: 'Admin User',
            role: 'admin'
        };

        const session: Session = {
            token: 'fake-jwt-token',
            user,
            issuedAt: now.toISOString(),
            expiresAt: expires.toISOString()
        };

        return { kind: 'success', session };
    }

    return {
        kind: 'failure',
        reason: 'invalid_credentials',
        message: 'Invalid email or password.'
    };
}
