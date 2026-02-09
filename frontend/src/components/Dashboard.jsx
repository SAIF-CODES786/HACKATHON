import React, { useState } from 'react';
import { Trophy, Mail, Phone, Award, Briefcase, GraduationCap, Filter, Download, Eye } from 'lucide-react';

const Dashboard = ({ candidates, onExport, onViewDetails }) => {
    const [minScore, setMinScore] = useState(0);
    const [sortBy, setSortBy] = useState('rank');

    const filteredCandidates = candidates
        .filter(c => c.total_score >= minScore)
        .sort((a, b) => {
            if (sortBy === 'rank') return a.rank - b.rank;
            if (sortBy === 'experience') return b.years_of_experience - a.years_of_experience;
            if (sortBy === 'education') return b.education_score - a.education_score;
            return 0;
        });

    const getScoreColor = (score) => {
        if (score >= 80) return 'text-green-600 bg-green-100';
        if (score >= 60) return 'text-blue-600 bg-blue-100';
        if (score >= 40) return 'text-yellow-600 bg-yellow-100';
        return 'text-red-600 bg-red-100';
    };

    const getRankBadge = (rank) => {
        if (rank === 1) return '🥇';
        if (rank === 2) return '🥈';
        if (rank === 3) return '🥉';
        return `#${rank}`;
    };

    if (candidates.length === 0) {
        return (
            <div className="card text-center py-12 animate-fade-in">
                <Trophy className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-600 mb-2">No Candidates Yet</h3>
                <p className="text-gray-500">Upload resumes and score them to see rankings here</p>
            </div>
        );
    }

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Header with filters */}
            <div className="card">
                <div className="flex flex-wrap items-center justify-between gap-4">
                    <div>
                        <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
                            <Trophy className="w-6 h-6 text-yellow-500" />
                            Candidate Rankings
                        </h2>
                        <p className="text-sm text-gray-600 mt-1">
                            {filteredCandidates.length} of {candidates.length} candidates shown
                        </p>
                    </div>

                    <div className="flex gap-3">
                        <button
                            onClick={() => onExport('csv')}
                            className="btn-secondary flex items-center gap-2"
                        >
                            <Download className="w-4 h-4" />
                            Export CSV
                        </button>
                        <button
                            onClick={() => onExport('excel')}
                            className="btn-secondary flex items-center gap-2"
                        >
                            <Download className="w-4 h-4" />
                            Export Excel
                        </button>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                            <Filter className="w-4 h-4" />
                            Minimum Score
                        </label>
                        <input
                            type="range"
                            min="0"
                            max="100"
                            value={minScore}
                            onChange={(e) => setMinScore(parseInt(e.target.value))}
                            className="w-full"
                        />
                        <div className="flex justify-between text-xs text-gray-600 mt-1">
                            <span>0</span>
                            <span className="font-semibold text-primary-600">{minScore}</span>
                            <span>100</span>
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-2">
                            Sort By
                        </label>
                        <select
                            value={sortBy}
                            onChange={(e) => setSortBy(e.target.value)}
                            className="input-field"
                        >
                            <option value="rank">Rank (Default)</option>
                            <option value="experience">Years of Experience</option>
                            <option value="education">Education Level</option>
                        </select>
                    </div>
                </div>
            </div>

            {/* Candidate cards */}
            <div className="grid gap-4">
                {filteredCandidates.map((candidate, index) => (
                    <div
                        key={index}
                        className="card hover:scale-[1.01] transition-transform duration-200 animate-slide-up"
                        style={{ animationDelay: `${index * 50}ms` }}
                    >
                        <div className="flex items-start justify-between">
                            <div className="flex-1">
                                <div className="flex items-center gap-3 mb-3">
                                    <span className="text-3xl">{getRankBadge(candidate.rank)}</span>
                                    <div>
                                        <h3 className="text-xl font-bold text-gray-800">
                                            {candidate.name || 'Unknown Candidate'}
                                        </h3>
                                        <div className="flex flex-wrap gap-3 mt-1 text-sm text-gray-600">
                                            {candidate.email && (
                                                <span className="flex items-center gap-1">
                                                    <Mail className="w-4 h-4" />
                                                    {candidate.email}
                                                </span>
                                            )}
                                            {candidate.phone && (
                                                <span className="flex items-center gap-1">
                                                    <Phone className="w-4 h-4" />
                                                    {candidate.phone}
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                </div>

                                {/* Score breakdown */}
                                <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-4">
                                    <div className="text-center">
                                        <div className={`text-2xl font-bold rounded-lg py-2 ${getScoreColor(candidate.total_score)}`}>
                                            {candidate.total_score}
                                        </div>
                                        <p className="text-xs text-gray-600 mt-1 font-semibold">Total Score</p>
                                    </div>
                                    <div className="text-center">
                                        <div className="text-lg font-semibold text-primary-600">
                                            {candidate.skills_score}
                                        </div>
                                        <p className="text-xs text-gray-600 mt-1">Skills</p>
                                    </div>
                                    <div className="text-center">
                                        <div className="text-lg font-semibold text-green-600">
                                            {candidate.experience_score}
                                        </div>
                                        <p className="text-xs text-gray-600 mt-1">Experience</p>
                                    </div>
                                    <div className="text-center">
                                        <div className="text-lg font-semibold text-yellow-600">
                                            {candidate.education_score}
                                        </div>
                                        <p className="text-xs text-gray-600 mt-1">Education</p>
                                    </div>
                                    <div className="text-center">
                                        <div className="text-lg font-semibold text-purple-600">
                                            {candidate.certifications_score}
                                        </div>
                                        <p className="text-xs text-gray-600 mt-1">Certs</p>
                                    </div>
                                </div>

                                {/* Details */}
                                <div className="flex flex-wrap gap-4 text-sm">
                                    <div className="flex items-center gap-2">
                                        <Briefcase className="w-4 h-4 text-gray-500" />
                                        <span className="font-semibold">{candidate.years_of_experience || 0} years</span>
                                    </div>
                                    {candidate.education && candidate.education.length > 0 && (
                                        <div className="flex items-center gap-2">
                                            <GraduationCap className="w-4 h-4 text-gray-500" />
                                            <span>{candidate.education[0].degree}</span>
                                        </div>
                                    )}
                                    {candidate.certifications && candidate.certifications.length > 0 && (
                                        <div className="flex items-center gap-2">
                                            <Award className="w-4 h-4 text-gray-500" />
                                            <span>{candidate.certifications.length} certification(s)</span>
                                        </div>
                                    )}
                                </div>

                                {/* Skills */}
                                {candidate.skills && candidate.skills.length > 0 && (
                                    <div className="mt-3">
                                        <p className="text-xs font-semibold text-gray-600 mb-2">Skills:</p>
                                        <div className="flex flex-wrap gap-2">
                                            {candidate.skills.slice(0, 8).map((skill, i) => (
                                                <span key={i} className="badge-info">
                                                    {skill}
                                                </span>
                                            ))}
                                            {candidate.skills.length > 8 && (
                                                <span className="badge bg-gray-200 text-gray-700">
                                                    +{candidate.skills.length - 8} more
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                )}
                            </div>

                            <button
                                onClick={() => onViewDetails(index)}
                                className="ml-4 p-3 rounded-lg bg-primary-50 text-primary-600 hover:bg-primary-100 transition-colors"
                                title="View Details"
                            >
                                <Eye className="w-5 h-5" />
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Dashboard;
