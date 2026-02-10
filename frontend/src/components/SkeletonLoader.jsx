import React from 'react';

const SkeletonLoader = ({ type = 'dashboard' }) => {
    if (type === 'dashboard') {
        return (
            <div className="card p-6 space-y-4 animate-pulse">
                {/* Header skeleton */}
                <div className="flex justify-between items-center">
                    <div className="h-8 bg-gradient-to-r from-accent-200 to-accent-300 dark:from-accent-700 dark:to-accent-800 rounded w-48"></div>
                    <div className="h-10 bg-gradient-to-r from-accent-200 to-accent-300 dark:from-accent-700 dark:to-accent-800 rounded w-32"></div>
                </div>

                {/* Table header skeleton */}
                <div className="grid grid-cols-6 gap-4 py-3 border-b border-accent-200 dark:border-accent-700">
                    {[...Array(6)].map((_, i) => (
                        <div key={i} className="h-4 bg-gradient-to-r from-accent-200 to-accent-300 dark:from-accent-700 dark:to-accent-800 rounded"></div>
                    ))}
                </div>

                {/* Table rows skeleton */}
                {[...Array(5)].map((_, rowIndex) => (
                    <div key={rowIndex} className="grid grid-cols-6 gap-4 py-4">
                        {[...Array(6)].map((_, colIndex) => (
                            <div
                                key={colIndex}
                                className="h-4 bg-gradient-to-r from-accent-200 via-accent-100 to-accent-200 dark:from-accent-700 dark:via-accent-800 dark:to-accent-700 rounded animate-shimmer"
                                style={{
                                    backgroundSize: '1000px 100%',
                                    animationDelay: `${rowIndex * 0.1}s`
                                }}
                            ></div>
                        ))}
                    </div>
                ))}
            </div>
        );
    }

    if (type === 'analytics') {
        return (
            <div className="space-y-6">
                {/* Stats cards skeleton */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {[...Array(3)].map((_, i) => (
                        <div key={i} className="card p-6 animate-pulse">
                            <div className="h-4 bg-gradient-to-r from-accent-200 to-accent-300 dark:from-accent-700 dark:to-accent-800 rounded w-24 mb-3"></div>
                            <div className="h-8 bg-gradient-to-r from-accent-200 to-accent-300 dark:from-accent-700 dark:to-accent-800 rounded w-16"></div>
                        </div>
                    ))}
                </div>

                {/* Charts skeleton */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {[...Array(4)].map((_, i) => (
                        <div key={i} className="card p-6 animate-pulse">
                            <div className="h-6 bg-gradient-to-r from-accent-200 to-accent-300 dark:from-accent-700 dark:to-accent-800 rounded w-32 mb-4"></div>
                            <div className="h-64 bg-gradient-to-br from-accent-100 to-accent-200 dark:from-accent-800 dark:to-accent-900 rounded-lg"></div>
                        </div>
                    ))}
                </div>
            </div>
        );
    }

    return null;
};

export default SkeletonLoader;
