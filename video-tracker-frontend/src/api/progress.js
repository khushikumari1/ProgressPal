import axios from "axios";

// Create axios instance with base URL
const api = axios.create({
    baseURL: "http://localhost:8000", // or your API_BASE_URL
});

// Automatically add JWT token to every request
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

/**
 * Save user's video progress
 * @param {string} videoId - ID of the video
 * @param {Array} watchedIntervals - List of watched intervals [{start: number, end: number}]
 * @param {number} lastWatched - Last watched timestamp (optional)
 */
export const saveProgress = (videoId, watchedIntervals, lastWatched = null) => {
    return api.post("/progress", {
        video_id: videoId,
        watched_intervals: watchedIntervals,
        last_watched: lastWatched,
    });
};

/**
 * Get user's progress for a specific video
 * @param {string} videoId - ID of the video
 */
export const getProgress = (videoId) => {
    return api.get("/progress", {
        params: { video_id: videoId },
    }).then(res => res.data);
};
