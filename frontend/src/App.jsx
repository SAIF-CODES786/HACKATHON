import React, { useState } from 'react';
import { api } from './services/api';
import UploadSection from './components/UploadSection';
import JobDescriptionForm from './components/JobDescriptionForm';
import Dashboard from './components/Dashboard';
import Analytics from './components/Analytics';
import CandidateDetail from './components/CandidateDetail';
import { FileSearch, BarChart3, Trash2 } from 'lucide-react';

function App() {
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const [candidates, setCandidates] = useState([]);
    const [selectedCandidate, setSelectedCandidate] = useState(null);
    const [activeTab, setActiveTab] = useState('dashboard'); // dashboard or analytics
    const [isUploading, setIsUploading] = useState(false);
    const [isScoring, setIsScoring] = useState(false);
    const [notification, setNotification] = useState(null);

    const showNotification = (message, type = 'success') => {
        setNotification({ message, type });
        setTimeout(() => setNotification(null), 4000);
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
        <div className="min-h-screen py-8 px-4">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="text-center mb-8 animate-fade-in">
                    <div className="flex items-center justify-center gap-3 mb-3">
                        <FileSearch className="w-12 h-12 text-white" />
                        <h1 className="text-5xl font-extrabold text-white drop-shadow-lg">
                            Resume Screening System
                        </h1>
                    </div>
                    <p className="text-xl text-white text-opacity-90 font-medium">
                        AI-Powered Candidate Ranking & Analysis
                    </p>
                </div>

                {/* Notification */}
                {notification && (
                    <div className={`fixed top-4 right-4 z-50 px-6 py-4 rounded-lg shadow-lg animate-slide-up ${notification.type === 'success' ? 'bg-green-500' :
                            notification.type === 'warning' ? 'bg-yellow-500' :
                                'bg-red-500'
                        } text-white font-semibold`}>
                        {notification.message}
                    </div>
                )}

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

                        <JobDescriptionForm
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
                            <Dashboard
                                candidates={candidates}
                                onExport={handleExport}
                                onViewDetails={handleViewDetails}
                            />
                        ) : (
                            <Analytics candidates={candidates} />
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
