import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
    children: ReactNode;
}

interface State {
    hasError: boolean;
    error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
    public state: State = {
        hasError: false,
        error: null
    };

    public static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error };
    }

    public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error('Uncaught error:', error, errorInfo);
    }

    public render() {
        if (this.state.hasError) {
            return (
                <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white p-6">
                    <div className="max-w-lg w-full bg-gray-800 border border-red-500/30 rounded-lg p-6 shadow-2xl">
                        <h1 className="text-2xl font-bold text-red-500 mb-4">Something went wrong</h1>
                        <p className="text-gray-300 mb-4">
                            The application encountered an unexpected error.
                        </p>
                        <div className="bg-black/50 p-4 rounded overflow-auto mb-6 text-sm font-mono text-red-300 max-h-48 border border-white/10">
                            {this.state.error?.message}
                        </div>
                        <div className="flex gap-4">
                            <button
                                onClick={() => window.location.reload()}
                                className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded transition-colors"
                            >
                                Reload Page
                            </button>
                            <button
                                onClick={() => {
                                    navigator.clipboard.writeText(this.state.error?.message || "Unknown Error");
                                    alert("Error copied to clipboard");
                                }}
                                className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded transition-colors"
                            >
                                Copy Error
                            </button>
                        </div>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}
