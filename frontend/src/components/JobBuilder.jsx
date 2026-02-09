import React, { useState } from 'react';
import { Briefcase, TrendingUp, X, Plus, Sparkles } from 'lucide-react';

const JobBuilder = ({ onSubmit, isLoading }) => {
    const [jobRole, setJobRole] = useState('');
    const [experienceRange, setExperienceRange] = useState([0, 5]);
    const [skills, setSkills] = useState([]);
    const [skillInput, setSkillInput] = useState('');

    const jobRoles = [
        {
            value: 'fullstack',
            label: 'Full Stack Developer',
            skills: ['JavaScript', 'React', 'Node.js', 'MongoDB', 'Express', 'Git']
        },
        {
            value: 'frontend',
            label: 'Frontend Developer',
            skills: ['React', 'JavaScript', 'HTML', 'CSS', 'Tailwind', 'TypeScript']
        },
        {
            value: 'backend',
            label: 'Backend Developer',
            skills: ['Python', 'Node.js', 'SQL', 'MongoDB', 'REST API', 'Docker']
        },
        {
            value: 'datascientist',
            label: 'Data Scientist',
            skills: ['Python', 'Machine Learning', 'Pandas', 'Numpy', 'TensorFlow', 'SQL']
        },
        {
            value: 'devops',
            label: 'DevOps Engineer',
            skills: ['Docker', 'Kubernetes', 'AWS', 'Jenkins', 'Git', 'Linux']
        }
    ];

    const handleRoleChange = (e) => {
        const selectedRole = e.target.value;
        setJobRole(selectedRole);

        // Auto-fill skills based on role
        const role = jobRoles.find(r => r.value === selectedRole);
        if (role) {
            setSkills(role.skills);
        }
    };

    const handleAddSkill = () => {
        if (skillInput.trim() && !skills.includes(skillInput.trim())) {
            setSkills([...skills, skillInput.trim()]);
            setSkillInput('');
        }
    };

    const handleRemoveSkill = (skillToRemove) => {
        setSkills(skills.filter(skill => skill !== skillToRemove));
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleAddSkill();
        }
    };

    const generateDescription = () => {
        const roleLabel = jobRoles.find(r => r.value === jobRole)?.label || 'Professional';
        const skillsList = skills.join(', ');
        return `Looking for a ${roleLabel} with ${experienceRange[0]}-${experienceRange[1]} years of experience. Required skills: ${skillsList}. The ideal candidate should have strong problem-solving abilities and excellent communication skills.`;
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const description = generateDescription();
        onSubmit({
            description,
            required_skills: skills,
            min_experience: experienceRange[0],
            max_experience: experienceRange[1]
        });
    };

    return (
        <div className="card animate-fade-in">
            <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-gradient-to-br from-primary-500 to-accent-500 rounded-xl">
                    <Briefcase className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100">Job Builder</h2>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Define your ideal candidate</p>
                </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
                {/* Job Role Dropdown */}
                <div>
                    <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                        Job Role
                    </label>
                    <select
                        value={jobRole}
                        onChange={handleRoleChange}
                        className="input-field"
                        required
                    >
                        <option value="">Select a role...</option>
                        {jobRoles.map(role => (
                            <option key={role.value} value={role.value}>
                                {role.label}
                            </option>
                        ))}
                    </select>
                </div>

                {/* Experience Range Slider */}
                <div>
                    <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                        Experience Level: {experienceRange[0]} - {experienceRange[1]} Years
                    </label>
                    <div className="space-y-4">
                        <div className="flex gap-4">
                            <div className="flex-1">
                                <label className="text-xs text-gray-600 dark:text-gray-400 mb-1 block">Min Years</label>
                                <input
                                    type="range"
                                    min="0"
                                    max="15"
                                    value={experienceRange[0]}
                                    onChange={(e) => setExperienceRange([parseInt(e.target.value), Math.max(parseInt(e.target.value), experienceRange[1])])}
                                    className="w-full h-3 bg-gradient-to-r from-primary-200 to-primary-400 dark:from-primary-800 dark:to-primary-600 rounded-lg appearance-none cursor-pointer accent-primary-600"
                                />
                            </div>
                            <div className="flex-1">
                                <label className="text-xs text-gray-600 dark:text-gray-400 mb-1 block">Max Years</label>
                                <input
                                    type="range"
                                    min="0"
                                    max="15"
                                    value={experienceRange[1]}
                                    onChange={(e) => setExperienceRange([experienceRange[0], Math.max(experienceRange[0], parseInt(e.target.value))])}
                                    className="w-full h-3 bg-gradient-to-r from-accent-200 to-accent-400 dark:from-accent-800 dark:to-accent-600 rounded-lg appearance-none cursor-pointer accent-accent-600"
                                />
                            </div>
                        </div>
                    </div>
                </div>

                {/* Skills Tag Input */}
                <div>
                    <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                        Required Skills
                    </label>
                    <div className="flex gap-2 mb-3">
                        <input
                            type="text"
                            value={skillInput}
                            onChange={(e) => setSkillInput(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Type a skill and press Enter..."
                            className="input-field flex-1"
                        />
                        <button
                            type="button"
                            onClick={handleAddSkill}
                            className="p-3 bg-primary-600 hover:bg-primary-700 text-white rounded-xl transition-colors"
                        >
                            <Plus className="w-5 h-5" />
                        </button>
                    </div>

                    {/* Skills Tags */}
                    <div className="flex flex-wrap gap-2 min-h-[40px] p-3 border-2 border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900/50">
                        {skills.length === 0 ? (
                            <span className="text-sm text-gray-400 dark:text-gray-500">No skills added yet...</span>
                        ) : (
                            skills.map((skill, index) => (
                                <span
                                    key={index}
                                    className="inline-flex items-center gap-1 px-3 py-1 bg-gradient-to-r from-primary-500 to-accent-500 text-white text-sm font-medium rounded-full group hover:from-primary-600 hover:to-accent-600 transition-all"
                                >
                                    {skill}
                                    <button
                                        type="button"
                                        onClick={() => handleRemoveSkill(skill)}
                                        className="ml-1 hover:bg-white/20 rounded-full p-0.5 transition-colors"
                                    >
                                        <X className="w-3 h-3" />
                                    </button>
                                </span>
                            ))
                        )}
                    </div>
                </div>

                {/* Submit Button */}
                <button
                    type="submit"
                    disabled={isLoading || !jobRole || skills.length === 0}
                    className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                    {isLoading ? (
                        <>
                            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                            Scoring Candidates...
                        </>
                    ) : (
                        <>
                            <Sparkles className="w-5 h-5" />
                            Score Candidates
                        </>
                    )}
                </button>
            </form>
        </div>
    );
};

export default JobBuilder;
