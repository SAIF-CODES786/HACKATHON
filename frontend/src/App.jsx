import React, { useState } from 'react';
import { api } from './services/api';
import UploadSection from './components/UploadSection';
import JobBuilder from './components/JobBuilder';
import Dashboard from './components/Dashboard';
import Analytics from './components/Analytics';
import CandidateDetail from './components/CandidateDetail';
import ErrorBoundary from './components/ErrorBoundary';
import { FileSearch, BarChart3, Trash2, Sun, Moon } from 'lucide-react';
import { useTheme } from './context/ThemeContext';
import { Toaster, toast } from 'react-hot-toast';
import { AnimatePresence, motion } from 'framer-motion';

function App() {
    return (
        <ErrorBoundary>
            <Toaster />
            <AppContent />
        </ErrorBoundary>
    );
}

function AppContent() {
    const { isDark, toggleTheme } = useTheme();
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const [candidates, setCandidates] = useState([]);
    const [selectedCandidate, setSelectedCandidate] = useState(null);
    const [activeTab, setActiveTab] = useState('dashboard'); // dashboard or analytics
    const [isUploading, setIsUploading] = useState(false);
    const [isScoring, setIsScoring] = useState(false);

    const showNotification = (message, type = 'success') => {
        if (type === 'success') {
            toast.success(message, {
                duration: 4000,
                position: 'top-right',
                style: {
                    background: '#10b981',
                    color: '#fff',
                    fontWeight: '600',
                },
            });
        } else if (type === 'error') {
            toast.error(message, {
                duration: 4000,
                position: 'top-right',
                style: {
                    background: '#ef4444',
                    color: '#fff',
                    fontWeight: '600',
                },
            });
        } else if (type === 'warning') {
            toast(message, {
                duration: 4000,
                position: 'top-right',
                icon: '⚠️',
                style: {
                    background: '#f59e0b',
                    color: '#fff',
                    fontWeight: '600',
                },
            });
        }
    };

    const handleUpload = async (files) => {
        setIsUploading(true);
        try {
            const result = await api.uploadResumes(files);
            showNotification(`Successfully uploaded ${result.success} resume(s)!`);
            setUploadedFiles([]);

            if (result.errors.length > 0) {
                showNotification(`${result.errors.length} file(s) failed to upload`, 'warning');
            }
        } catch (error) {
            showNotification('Failed to upload resumes. Please try again.', 'error');
            console.error('Upload error:', error);
        } finally {
            setIsUploading(false);
        }
    };

    const handleScore = async (jobData) => {
        setIsScoring(true);
        try {
            const result = await api.scoreCandidates(jobData);
            setCandidates(result.candidates);
            setActiveTab('dashboard');
            showNotification(`Successfully scored ${result.total_candidates} candidate(s)!`);
        } catch (error) {
            showNotification('Failed to score candidates. Please try again.', 'error');
            console.error('Scoring error:', error);
        } finally {
            setIsScoring(false);
        }
    };

    const handleExport = async (format) => {
        try {
            await api.exportResults(format);
            showNotification(`Successfully exported results as ${format.toUpperCase()}!`);
        } catch (error) {
            showNotification('Failed to export results. Please try again.', 'error');
            console.error('Export error:', error);
        }
    };

    const handleViewDetails = (index) => {
        setSelectedCandidate(candidates[index]);
    };

    const handleClearData = async () => {
        if (window.confirm('Are you sure you want to clear all data? This cannot be undone.')) {
            try {
                await api.clearData();
                setCandidates([]);
                setUploadedFiles([]);
                showNotification('All data cleared successfully!');
            } catch (error) {
                showNotification('Failed to clear data. Please try again.', 'error');
                console.error('Clear error:', error);
            }
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300 py-8 px-4">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="text-center mb-8 animate-fade-in relative">
                    {/* Theme Toggle */}
                    <button
                        onClick={toggleTheme}
                        className="absolute right-0 top-0 p-3 rounded-xl bg-white/10 dark:bg-gray-800/50 backdrop-blur-sm border border-white/20 dark:border-gray-700 hover:bg-white/20 dark:hover:bg-gray-700/50 transition-all duration-300 group"
                        aria-label="Toggle theme"
                    >
                        {isDark ? (
                            <Sun className="w-6 h-6 text-yellow-400 group-hover:rotate-180 transition-transform duration-500" />
                        ) : (
                            <Moon className="w-6 h-6 text-blue-200 group-hover:-rotate-12 transition-transform duration-500" />
                        )}
                    </button>

                    <div className="flex items-center justify-center gap-3 mb-3">
                        <FileSearch className="w-12 h-12 text-primary-400 dark:text-primary-300" />
                        <h1 className="text-5xl font-extrabold bg-gradient-to-r from-primary-600 to-accent-600 dark:from-primary-400 dark:to-accent-400 bg-clip-text text-transparent drop-shadow-lg">
                            Resume Screening System
                        </h1>
                    </div>
                    <p className="text-xl text-gray-700 dark:text-gray-300 font-medium">
                        AI-Powered Candidate Ranking & Analysis
                    </p>
                </div>



                {/* Main Content */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                    {/* Left Column - Upload & Job Description */}
                    <div className="lg:col-span-1 space-y-6">
                        <UploadSection
                            onUpload={handleUpload}
                            uploadedFiles={uploadedFiles}
                            setUploadedFiles={setUploadedFiles}
                            isLoading={isUploading}
                        />

                        <JobBuilder
                            onSubmit={handleScore}
                            isLoading={isScoring}
                        />

                        {candidates.length > 0 && (
                            <button
                                onClick={handleClearData}
                                className="w-full btn-secondary flex items-center justify-center gap-2 bg-red-50 text-red-600 border-red-200 hover:bg-red-100 hover:border-red-400"
                            >
                                <Trash2 className="w-4 h-4" />
                                Clear All Data
                            </button>
                        )}
                    </div>

                    {/* Right Column - Dashboard & Analytics */}
                    <div className="lg:col-span-2">
                        {candidates.length > 0 && (
                            <div className="mb-6">
                                <div className="card p-2">
                                    <div className="flex gap-2">
                                        <button
                                            onClick={() => setActiveTab('dashboard')}
                                            className={`flex-1 py-3 px-4 rounded-lg font-semibold transition-all ${activeTab === 'dashboard'
                                                ? 'bg-gradient-to-r from-primary-600 to-accent-600 text-white shadow-md'
                                                : 'text-gray-600 hover:bg-gray-100'
                                                }`}
                                        >
                                            <FileSearch className="w-5 h-5 inline mr-2" />
                                            Rankings
                                        </button>
                                        <button
                                            onClick={() => setActiveTab('analytics')}
                                            className={`flex-1 py-3 px-4 rounded-lg font-semibold transition-all ${activeTab === 'analytics'
                                                ? 'bg-gradient-to-r from-primary-600 to-accent-600 text-white shadow-md'
                                                : 'text-gray-600 hover:bg-gray-100'
                                                }`}
                                        >
                                            <BarChart3 className="w-5 h-5 inline mr-2" />
                                            Analytics
                                        </button>
                                    </div>
                                </div>
                            </div>
                        )}

                        {activeTab === 'dashboard' ? (
                            <AnimatePresence mode="wait">
                                <motion.div
                                    key="dashboard"
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: -20 }}
                                    transition={{ duration: 0.3 }}
                                >
                                    <Dashboard
                                        candidates={candidates}
                                        onExport={handleExport}
                                        onViewDetails={handleViewDetails}
                                    />
                                </motion.div>
                            </AnimatePresence>
                        ) : (
                            <AnimatePresence mode="wait">
                                <motion.div
                                    key="analytics"
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: -20 }}
                                    transition={{ duration: 0.3 }}
                                >
                                    <Analytics candidates={candidates} />
                                </motion.div>
                            </AnimatePresence>
                        )}
                    </div>
                </div>

                {/* Footer */}
                <div className="text-center text-white text-opacity-80 mt-12">
                    <p className="text-sm">
                        Built with React, FastAPI, and Machine Learning • Powered by TF-IDF & Cosine Similarity
                    </p>
                </div>
            </div>

            {/* Candidate Detail Modal */}
            {selectedCandidate && (
                <CandidateDetail
                    candidate={selectedCandidate}
                    onClose={() => setSelectedCandidate(null)}
                />
            )}
        </div>
    );
}

export default App;
