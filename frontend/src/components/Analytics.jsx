import React, { useState, useEffect } from 'react';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, Users, Award, Briefcase } from 'lucide-react';

const Analytics = ({ candidates }) => {
    const [stats, setStats] = useState(null);
    const [skillData, setSkillData] = useState([]);
    const [experienceData, setExperienceData] = useState([]);

    useEffect(() => {
        if (candidates.length > 0) {
            calculateAnalytics();
        }
    }, [candidates]);

    const calculateAnalytics = () => {
        // Calculate summary statistics
        const scores = candidates.map(c => c.total_score || 0);
        const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;
        const maxScore = Math.max(...scores);
        const minScore = Math.min(...scores);

        // Skill distribution
        const skillCount = {};
        candidates.forEach(c => {
            (c.skills || []).forEach(skill => {
                skillCount[skill] = (skillCount[skill] || 0) + 1;
            });
        });
        const topSkills = Object.entries(skillCount)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10)
            .map(([name, count]) => ({ name, count }));

        // Experience distribution
        const expLevels = {
            'Entry (0-2)': 0,
            'Junior (2-5)': 0,
            'Mid (5-8)': 0,
            'Senior (8-12)': 0,
            'Expert (12+)': 0
        };
        candidates.forEach(c => {
            const years = c.years_of_experience || 0;
            if (years <= 2) expLevels['Entry (0-2)']++;
            else if (years <= 5) expLevels['Junior (2-5)']++;
            else if (years <= 8) expLevels['Mid (5-8)']++;
            else if (years <= 12) expLevels['Senior (8-12)']++;
            else expLevels['Expert (12+)']++;
        });

        const expData = Object.entries(expLevels)
            .filter(([_, value]) => value > 0)
            .map(([name, value]) => ({ name, value }));

        setStats({
            total: candidates.length,
            avgScore: avgScore.toFixed(1),
            maxScore: maxScore.toFixed(1),
            minScore: minScore.toFixed(1)
        });
        setSkillData(topSkills);
        setExperienceData(expData);
    };

    const COLORS = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#3b82f6', '#ef4444', '#14b8a6', '#f97316', '#84cc16'];

    if (!stats) {
        return (
            <div className="card text-center py-12">
                <TrendingUp className="w-16 h-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-600 dark:text-gray-400 mb-2">No Analytics Available</h3>
                <p className="text-gray-500 dark:text-gray-500">Score candidates to view analytics</p>
            </div>
        );
    }

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Summary Statistics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="card bg-gradient-to-br from-blue-500 to-blue-600 text-white">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-blue-100 text-sm font-medium">Total Candidates</p>
                            <p className="text-3xl font-bold mt-1">{stats.total}</p>
                        </div>
                        <Users className="w-12 h-12 text-blue-200 opacity-80" />
                    </div>
                </div>

                <div className="card bg-gradient-to-br from-green-500 to-green-600 text-white">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-green-100 text-sm font-medium">Average Score</p>
                            <p className="text-3xl font-bold mt-1">{stats.avgScore}</p>
                        </div>
                        <TrendingUp className="w-12 h-12 text-green-200 opacity-80" />
                    </div>
                </div>

                <div className="card bg-gradient-to-br from-purple-500 to-purple-600 text-white">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-purple-100 text-sm font-medium">Highest Score</p>
                            <p className="text-3xl font-bold mt-1">{stats.maxScore}</p>
                        </div>
                        <Award className="w-12 h-12 text-purple-200 opacity-80" />
                    </div>
                </div>

                <div className="card bg-gradient-to-br from-orange-500 to-orange-600 text-white">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-orange-100 text-sm font-medium">Lowest Score</p>
                            <p className="text-3xl font-bold mt-1">{stats.minScore}</p>
                        </div>
                        <Briefcase className="w-12 h-12 text-orange-200 opacity-80" />
                    </div>
                </div>
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Skill Distribution */}
                <div className="card">
                    <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4">Top Skills Distribution</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={skillData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                            <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} stroke="#9ca3af" />
                            <YAxis stroke="#9ca3af" />
                            <Tooltip contentStyle={{ backgroundColor: 'rgba(255, 255, 255, 0.95)', border: '1px solid #e5e7eb', borderRadius: '8px' }} />
                            <Bar dataKey="count" fill="#6366f1" radius={[8, 8, 0, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                {/* Experience Distribution */}
                <div className="card">
                    <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4">Experience Level Distribution</h3>
                    <ResponsiveContainer width="100%" height={350}>
                        <PieChart margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                            <Pie
                                data={experienceData}
                                cx="50%"
                                cy="45%"
                                outerRadius={80}
                                fill="#8884d8"
                                dataKey="value"
                                label={false}
                            >
                                {experienceData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                            </Pie>
                            <Tooltip
                                formatter={(value, name, props) => [`${value} candidates`, props.payload.name]}
                            />
                            <Legend
                                verticalAlign="bottom"
                                height={36}
                                formatter={(value, entry) => `${value}: ${entry.payload.value}`}
                            />
                        </PieChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};

export default Analytics;
