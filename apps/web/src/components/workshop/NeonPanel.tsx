import React from 'react';
import { cn } from '../../lib/utils';

type NeonPanelProps = React.HTMLAttributes<HTMLDivElement> & {
    variant?: 'cyan' | 'violet' | 'subtle';
};

export function NeonPanel({
    className,
    variant = 'cyan',
    children,
    ...props
}: NeonPanelProps) {
    const variantClasses =
        variant === 'violet'
            ? 'border-workshop-violet/60 shadow-workshop-violet'
            : variant === 'subtle'
                ? 'border-white/5 shadow-none'
                : 'border-workshop-cyan/60 shadow-workshop-neon';

    return (
        <div
            className={cn(
                'relative rounded-workshop border bg-workshop-panel/80',
                'backdrop-blur-md',
                variantClasses,
                className
            )}
            {...props}
        >
            {children}
        </div>
    );
}
