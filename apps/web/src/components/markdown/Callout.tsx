import React from 'react';
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert';
import { AlertTriangle, Info } from 'lucide-react';

interface CalloutProps {
    variant: 'info' | 'warning';
    title?: string;
    children: React.ReactNode;
}

export function Callout({ variant, title, children }: CalloutProps) {
    const Icon = variant === 'warning' ? AlertTriangle : Info;

    return (
        <Alert variant={variant} className="my-6">
            <Icon className="h-4 w-4" />
            {title && <AlertTitle>{title}</AlertTitle>}
            <AlertDescription className="mt-2 text-sm">
                {children}
            </AlertDescription>
        </Alert>
    );
}
