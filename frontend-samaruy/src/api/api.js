// services/api.js
import axios from 'axios';

// Create an Axios instance
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000', // Adjust the base URL as needed
    headers: {
        'Content-Type': 'application/json',
    },
});

// Helper function to log errors
const logError = (error) => {
    console.error('API Error:', error);
    if (error.response) {
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
        console.error('Response headers:', error.response.headers);
    } else if (error.request) {
        console.error('Request data:', error.request);
    } else {
        console.error('Error message:', error.message);
    }
};

// Separate audio
export const separateAudio = async (stemCount, file, master = false, genre = null) => {
    const formData = new FormData();
    formData.append('file', file);
    const params = new URLSearchParams();
    if (master) params.append('master', master);
    if (genre) params.append('genre', genre);

    try {
        const response = await api.post(`/api/separate/${stemCount}`, formData, {
            params,
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        logError(error);
        throw error.response ? error.response.data : new Error('Network Error');
    }
};

// Download separated stem
export const downloadStem = async (fileName) => {
    try {
        const response = await api.get(`/api/download/${fileName}`, {
            responseType: 'blob',
        });
        return response.data;
    } catch (error) {
        logError(error);
        throw error.response ? error.response.data : new Error('Network Error');
    }
};

// Search and filter separated stems
export const searchStems = async (query = null, stemType = null, page = 1, pageSize = 10) => {
    const params = new URLSearchParams();
    if (query) params.append('query', query);
    if (stemType) params.append('stem_type', stemType);
    params.append('page', page);
    params.append('page_size', pageSize);

    try {
        const response = await api.get('/api/search', {params});
        return response.data;
    } catch (error) {
        logError(error);
        throw error.response ? error.response.data : new Error('Network Error');
    }
};


export const getStemDetails = async (stemId) => {
    try {
        const response = await api.get(`/api/stems/${stemId}`);
        return response.data;
    } catch (error) {
        logError(error);
        throw error.response ? error.response.data : new Error('Network Error');
    }
};

export const getAllStems = async () => {
    try {
        const response = await api.get('/api/stems');
        return response.data;
    } catch (error) {
        logError(error);
        throw error.response ? error.response.data : new Error('Network Error');
    }
}

