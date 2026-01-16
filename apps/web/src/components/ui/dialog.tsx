import * as React from "react"
import { cn } from "@/lib/utils"

// Simple Custom Dialog to match Radix API structure without dependencies

interface DialogProps {
    open?: boolean;
    onOpenChange?: (open: boolean) => void;
    children: React.ReactNode;
}

const DialogContext = React.createContext<{
    open: boolean;
    onOpenChange: (open: boolean) => void;
}>({ open: false, onOpenChange: () => { } });

export function Dialog({ open = false, onOpenChange, children }: DialogProps) {
    return (
        <DialogContext.Provider value={{ open, onOpenChange: onOpenChange || (() => { }) }}>
            {children}
        </DialogContext.Provider>
    );
}

export function DialogContent({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
    const { open, onOpenChange } = React.useContext(DialogContext);

    if (!open) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
            {/* Backdrop */}
            <div
                className="fixed inset-0 bg-black/80 backdrop-blur-sm animate-in fade-in-0"
                onClick={() => onOpenChange(false)}
            />
            {/* Panel */}
            <div
                className={cn(
                    "relative z-50 grid w-full max-w-lg scale-100 gap-4 border border-slate-200 bg-white p-6 shadow-lg duration-200 animate-in fade-in-0 zoom-in-95 sm:rounded-lg md:w-full dark:border-slate-800 dark:bg-slate-950 text-slate-950 dark:text-slate-50",
                    className
                )}
                {...props}
            >
                {children}

                <button
                    className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-white transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-slate-950 focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-slate-100 data-[state=open]:text-slate-500 dark:ring-offset-slate-950 dark:focus:ring-slate-300 dark:data-[state=open]:bg-slate-800 dark:data-[state=open]:text-slate-400"
                    onClick={() => onOpenChange(false)}
                >
                    <span className="sr-only">Close</span>
                </button>
            </div>
        </div>
    )
}

export function DialogHeader({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
    return (
        <div className={cn("flex flex-col space-y-1.5 text-center sm:text-left", className)} {...props} />
    )
}

export function DialogTitle({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) {
    return (
        <h2 className={cn("text-lg font-semibold leading-none tracking-tight", className)} {...props} />
    )
}

export function DialogDescription({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) {
    return (
        <p className={cn("text-sm text-slate-500 dark:text-slate-400", className)} {...props} />
    )
}
