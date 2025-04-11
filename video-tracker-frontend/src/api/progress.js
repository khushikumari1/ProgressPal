// src/api/progress.js

import axios from "axios";
import { BACKEND_URL } from "../config";

export const fetchProgress = async (userId, videoId) => {
    const res = await axios.get(`${BACKEND_URL}/progress`, {
        params: { user_id: userId, video_id: videoId },
    });
    return res.data;
};

export const saveProgress = async (payload) => {
    const res = await axios.post(`${BACKEND_URL}/progress`, payload);
    return res.data;
};
