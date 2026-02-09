import React, { useState } from 'react';
import { Briefcase, Sparkles } from 'lucide-react';

const JobDescriptionForm = ({ onSubmit, isLoading }) => {
    const [formData, setFormData] = useState({
        description: '',
        required_skills: '',
        min_experience: 0,
        max_experience: 15
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <div className="card animate-fade-in">
            <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <Briefcase className="w-6 h-6 text-accent-600" />
                Job Description
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                        Job Description *
                    </label>
                    <textarea
                        value={formData.description}
                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                        className="input-field min-h-[150px] resize-y"
                        placeholder="Enter the full job description including responsibilities, requirements, and qualifications..."
                        required
                    />
                </div>

                <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                        Required Skills (comma-separated)
                    </label>
                    <input
                        type="text"
                        value={formData.required_skills}
                        onChange={(e) => setFormData({ ...formData, required_skills: e.target.value })}
                        className="input-field"
                        placeholder="e.g., Python, React, Machine Learning, AWS"
                    />
                    <p className="text-xs text-gray-500 mt-1">
                        Optional: Specify key skills for better matching accuracy
                    </p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-2">
                            Min Experience (years)
                        </label>
                        <input
                            type="number"
                            value={formData.min_experience}
                            onChange={(e) => setFormData({ ...formData, min_experience: parseFloat(e.target.value) })}
                            className="input-field"
                            min="0"
                            step="0.5"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-2">
                            Max Experience (years)
                        </label>
                        <input
                            type="number"
                            value={formData.max_experience}
                            onChange={(e) => setFormData({ ...formData, max_experience: parseFloat(e.target.value) })}
                            className="input-field"
                            min="0"
                            step="0.5"
                        />
                    </div>
                </div>

                <button
                    type="submit"
                    disabled={isLoading || !formData.description}
                    className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                    {isLoading ? (
                        <>
                            <div className="w-5 h-5 border-3 border-white border-t-transparent rounded-full animate-spin"></div>
                            Scoring Candidates...
                        </>
                    ) : (
                        <>
                            <Sparkles className="w-5 h-5" />
                            Score & Rank Candidates
                        </>
                    )}
                </button>
            </form>
        </div>
    );
};

export default JobDescriptionForm;
