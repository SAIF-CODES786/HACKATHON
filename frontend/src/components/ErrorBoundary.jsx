import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null, errorInfo: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        console.error('Error caught by boundary:', error, errorInfo);
        this.setState({
            error,
            errorInfo
        });
    }

    handleReload = () => {
        window.location.reload();
    };

    render() {
        if (this.state.hasError) {
            return (
                <div className="min-h-screen bg-gradient-to-br from-accent-50 to-primary-50 dark:from-accent-950 dark:to-primary-950 flex items-center justify-center p-4">
                    <div className="card max-w-lg w-full p-8 text-center space-y-6">
                        <div className="flex justify-center">
                            <div className="p-4 bg-red-100 dark:bg-red-900/30 rounded-full">
                                <AlertTriangle className="w-12 h-12 text-red-600 dark:text-red-400" />
                            </div>
                        </div>

                        <div>
                            <h1 className="text-2xl font-bold text-accent-900 dark:text-accent-100 mb-2">
                                Oops! Something went wrong
                            </h1>
                            <p className="text-accent-600 dark:text-accent-400">
                                We encountered an unexpected error. Please try reloading the page.
                            </p>
                        </div>

                        {process.env.NODE_ENV === 'development' && this.state.error && (
                            <details className="text-left bg-accent-100 dark:bg-accent-800 p-4 rounded-lg">
                                <summary className="cursor-pointer font-semibold text-accent-900 dark:text-accent-100 mb-2">
                                    Error Details
                                </summary>
                                <pre className="text-xs text-accent-700 dark:text-accent-300 overflow-auto">
                                    {this.state.error.toString()}
                                    {this.state.errorInfo && this.state.errorInfo.componentStack}
                                </pre>
                            </details>
                        )}

                        <button
                            onClick={this.handleReload}
                            className="btn-primary flex items-center justify-center gap-2 mx-auto"
                        >
                            <RefreshCw className="w-4 h-4" />
                            Reload Page
                        </button>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
