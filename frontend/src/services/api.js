import axios from 'axios';

const API_BASE_URL = '/api';

export const api = {
    // Upload resumes
    uploadResumes: async (files) => {
        const formData = new FormData();
        files.forEach(file => {
            formData.append('files', file);
        });

        const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    // Score candidates
    scoreCandidates: async (jobData) => {
        const formData = new FormData();
        formData.append('description', jobData.description);
        if (jobData.required_skills) {
            formData.append('required_skills', jobData.required_skills);
        }
        formData.append('min_experience', jobData.min_experience || 0);
        formData.append('max_experience', jobData.max_experience || 15);

        const response = await axios.post(`${API_BASE_URL}/score`, formData);
        return response.data;
    },

    // Get rankings
    getRankings: async (minScore = 0) => {
        const response = await axios.get(`${API_BASE_URL}/rankings`, {
            params: { min_score: minScore }
        });
        return response.data;
    },

    // Get analytics
    getAnalytics: async () => {
        const response = await axios.get(`${API_BASE_URL}/analytics`);
        return response.data;
    },

    // Export results
    exportResults: async (format = 'csv') => {
        const response = await axios.get(`${API_BASE_URL}/export`, {
            params: { format },
            responseType: 'blob'
        });

        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `candidates_ranked.${format}`);
        document.body.appendChild(link);
        link.click();
        link.remove();

        return true;
    },

    // Get candidate detail
    getCandidateDetail: async (candidateId) => {
        const response = await axios.get(`${API_BASE_URL}/candidate/${candidateId}`);
        return response.data;
    },

    // Clear all data
    clearData: async () => {
        const response = await axios.delete(`${API_BASE_URL}/clear`);
        return response.data;
    },

    // Health check
    healthCheck: async () => {
        const response = await axios.get(`${API_BASE_URL}/health`);
        return response.data;
    }
};
