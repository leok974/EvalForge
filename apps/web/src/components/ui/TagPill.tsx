import React from 'react';
import { cn } from "@/lib/utils";

export function TagPill({
    children,
    variant = "default",
    className,
}: {
    children: React.ReactNode;
    variant?: "default" | "world" | "docType";
    className?: string;
}) {
    return (
        <span
            className={cn(
                "inline-flex items-center rounded-full border px-3 py-1",
                "text-[10px] font-semibold uppercase tracking-[0.18em]",
                "shadow-sm",
                variant === "default" &&
                "border-zinc-500/50 bg-zinc-900/70 text-zinc-100",
                variant === "world" &&
                "border-cyan-500/60 bg-cyan-500/10 text-cyan-200",
                variant === "docType" &&
                "border-fuchsia-500/60 bg-fuchsia-500/10 text-fuchsia-200",
                className
            )}
        >
            {children}
        </span>
    );
}
