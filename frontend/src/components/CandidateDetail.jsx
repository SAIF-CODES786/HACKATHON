import React from 'react';
import { X, Mail, Phone, Award, Briefcase, GraduationCap, FileText } from 'lucide-react';

const CandidateDetail = ({ candidate, onClose }) => {
    if (!candidate) return null;

    const getScoreColor = (score) => {
        if (score >= 80) return 'text-green-600';
        if (score >= 60) return 'text-blue-600';
        if (score >= 40) return 'text-yellow-600';
        return 'text-red-600';
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 animate-fade-in">
            <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto animate-slide-up">
                {/* Header */}
                <div className="sticky top-0 bg-gradient-to-r from-primary-600 to-accent-600 text-white p-6 rounded-t-2xl flex items-center justify-between">
                    <div>
                        <h2 className="text-2xl font-bold">{candidate.name || 'Unknown Candidate'}</h2>
                        <p className="text-primary-100 mt-1">Rank #{candidate.rank}</p>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-white hover:bg-opacity-20 rounded-lg transition-colors"
                    >
                        <X className="w-6 h-6" />
                    </button>
                </div>

                <div className="p-6 space-y-6">
                    {/* Score Overview */}
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                        <div className="text-center p-4 bg-gradient-to-br from-primary-50 to-accent-50 rounded-xl">
                            <div className={`text-3xl font-bold ${getScoreColor(candidate.total_score)}`}>
                                {candidate.total_score}
                            </div>
                            <p className="text-sm text-gray-600 mt-1 font-semibold">Total Score</p>
                        </div>
                        <div className="text-center p-4 bg-blue-50 rounded-xl">
                            <div className="text-2xl font-bold text-blue-600">{candidate.skills_score}</div>
                            <p className="text-sm text-gray-600 mt-1">Skills</p>
                        </div>
                        <div className="text-center p-4 bg-green-50 rounded-xl">
                            <div className="text-2xl font-bold text-green-600">{candidate.experience_score}</div>
                            <p className="text-sm text-gray-600 mt-1">Experience</p>
                        </div>
                        <div className="text-center p-4 bg-yellow-50 rounded-xl">
                            <div className="text-2xl font-bold text-yellow-600">{candidate.education_score}</div>
                            <p className="text-sm text-gray-600 mt-1">Education</p>
                        </div>
                        <div className="text-center p-4 bg-purple-50 rounded-xl">
                            <div className="text-2xl font-bold text-purple-600">{candidate.certifications_score}</div>
                            <p className="text-sm text-gray-600 mt-1">Certifications</p>
                        </div>
                    </div>

                    {/* Contact Information */}
                    <div className="bg-gray-50 rounded-xl p-4">
                        <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
                            <Mail className="w-5 h-5 text-primary-600" />
                            Contact Information
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            {candidate.email && (
                                <div className="flex items-center gap-2">
                                    <Mail className="w-4 h-4 text-gray-500" />
                                    <span className="text-gray-700">{candidate.email}</span>
                                </div>
                            )}
                            {candidate.phone && (
                                <div className="flex items-center gap-2">
                                    <Phone className="w-4 h-4 text-gray-500" />
                                    <span className="text-gray-700">{candidate.phone}</span>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Skills */}
                    {candidate.skills && candidate.skills.length > 0 && (
                        <div>
                            <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
                                <Award className="w-5 h-5 text-primary-600" />
                                Skills ({candidate.skills.length})
                            </h3>
                            <div className="flex flex-wrap gap-2">
                                {candidate.skills.map((skill, i) => (
                                    <span key={i} className="badge-info text-sm">
                                        {skill}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Experience */}
                    <div>
                        <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
                            <Briefcase className="w-5 h-5 text-primary-600" />
                            Work Experience
                        </h3>
                        <div className="bg-gray-50 rounded-xl p-4">
                            <p className="text-gray-700">
                                <span className="font-semibold">Total Experience:</span> {candidate.years_of_experience || 0} years
                            </p>
                            {candidate.experience && candidate.experience.length > 0 && (
                                <div className="mt-3 space-y-2">
                                    {candidate.experience.map((exp, i) => (
                                        <div key={i} className="border-l-4 border-primary-400 pl-3">
                                            <p className="font-semibold text-gray-800">{exp.company}</p>
                                            {exp.position && <p className="text-sm text-gray-600">{exp.position}</p>}
                                            {exp.duration && <p className="text-xs text-gray-500">{exp.duration}</p>}
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Education */}
                    {candidate.education && candidate.education.length > 0 && (
                        <div>
                            <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
                                <GraduationCap className="w-5 h-5 text-primary-600" />
                                Education
                            </h3>
                            <div className="space-y-3">
                                {candidate.education.map((edu, i) => (
                                    <div key={i} className="bg-gray-50 rounded-xl p-4">
                                        <p className="font-semibold text-gray-800">{edu.degree}</p>
                                        {edu.institution && <p className="text-sm text-gray-600 mt-1">{edu.institution}</p>}
                                        {edu.year && <p className="text-xs text-gray-500 mt-1">{edu.year}</p>}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Certifications */}
                    {candidate.certifications && candidate.certifications.length > 0 && (
                        <div>
                            <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
                                <Award className="w-5 h-5 text-primary-600" />
                                Certifications
                            </h3>
                            <div className="space-y-2">
                                {candidate.certifications.map((cert, i) => (
                                    <div key={i} className="bg-gray-50 rounded-lg p-3 flex items-center gap-2">
                                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                                        <span className="text-gray-700">{cert}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Score Breakdown */}
                    {candidate.breakdown && (
                        <div>
                            <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
                                <FileText className="w-5 h-5 text-primary-600" />
                                Score Breakdown
                            </h3>
                            <div className="bg-gray-50 rounded-xl p-4 space-y-2 font-mono text-sm">
                                {Object.entries(candidate.breakdown).map(([key, value]) => (
                                    <div key={key} className="flex justify-between">
                                        <span className="text-gray-600 capitalize">{key}:</span>
                                        <span className="text-gray-800 font-semibold">{value}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default CandidateDetail;
