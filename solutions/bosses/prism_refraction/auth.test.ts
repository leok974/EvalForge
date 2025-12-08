// src/boss/typeGuardian/auth.ts
import { authenticate, isAuthSuccess, isAuthFailure, Credentials } from './auth';

describe('Type Guardian – auth module', () => {
    it('returns success for valid admin credentials', async () => {
        const creds: Credentials = {
            email: 'admin@example.com',
            password: 'password123'
        };

        const result = await authenticate(creds);

        expect(isAuthSuccess(result)).toBe(true);
        if (isAuthSuccess(result)) {
            expect(result.session.user.email).toBe('admin@example.com');
            expect(result.session.user.role).toBe('admin');
        }
    });

    it('returns failure for invalid credentials', async () => {
        const result = await authenticate({
            email: 'wrong@example.com',
            password: 'nope'
        });

        expect(isAuthFailure(result)).toBe(true);
        if (isAuthFailure(result)) {
            expect(result.reason).toBe('invalid_credentials');
            expect(result.message).toBeTruthy();
        }
    });
});
