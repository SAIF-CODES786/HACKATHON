import React, { useState } from 'react';
import { Lock, Mail, User, LogIn, UserPlus } from 'lucide-react';

const AuthPage = ({ onLogin }) => {
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        username: '',
        fullName: ''
    });

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Mock authentication - replace with actual API call
        if (isLogin) {
            // Login
            const mockToken = 'mock-jwt-token';
            localStorage.setItem('auth_token', mockToken);
            onLogin({ email: formData.email, token: mockToken });
        } else {
            // Register
            alert('Registration successful! Please login.');
            setIsLogin(true);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center py-12 px-4">
            <div className="max-w-md w-full">
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-extrabold text-white mb-2">
                        Resume Screening System
                    </h1>
                    <p className="text-white text-opacity-80">
                        {isLogin ? 'Sign in to your account' : 'Create a new account'}
                    </p>
                </div>

                <div className="card">
                    <form onSubmit={handleSubmit} className="space-y-4">
                        {!isLogin && (
                            <>
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                                        Full Name
                                    </label>
                                    <div className="relative">
                                        <User className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
                                        <input
                                            type="text"
                                            value={formData.fullName}
                                            onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                                            className="input-field pl-10"
                                            placeholder="John Doe"
                                            required={!isLogin}
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                                        Username
                                    </label>
                                    <div className="relative">
                                        <User className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
                                        <input
                                            type="text"
                                            value={formData.username}
                                            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                                            className="input-field pl-10"
                                            placeholder="johndoe"
                                            required={!isLogin}
                                        />
                                    </div>
                                </div>
                            </>
                        )}

                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-2">
                                Email Address
                            </label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
                                <input
                                    type="email"
                                    value={formData.email}
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    className="input-field pl-10"
                                    placeholder="you@example.com"
                                    required
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-2">
                                Password
                            </label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
                                <input
                                    type="password"
                                    value={formData.password}
                                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                    className="input-field pl-10"
                                    placeholder="••••••••"
                                    required
                                />
                            </div>
                        </div>

                        <button type="submit" className="btn-primary w-full flex items-center justify-center gap-2">
                            {isLogin ? (
                                <>
                                    <LogIn className="w-5 h-5" />
                                    Sign In
                                </>
                            ) : (
                                <>
                                    <UserPlus className="w-5 h-5" />
                                    Create Account
                                </>
                            )}
                        </button>
                    </form>

                    <div className="mt-6 text-center">
                        <button
                            onClick={() => setIsLogin(!isLogin)}
                            className="text-primary-600 hover:text-primary-700 font-semibold"
                        >
                            {isLogin ? "Don't have an account? Sign up" : 'Already have an account? Sign in'}
                        </button>
                    </div>
                </div>

                <div className="mt-6 text-center text-white text-opacity-70 text-sm">
                    <p>Demo credentials: any email/password</p>
                </div>
            </div>
        </div>
    );
};

export default AuthPage;
