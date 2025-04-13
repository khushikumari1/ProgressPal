import axios from "axios";
const BASE_URL = "http://localhost:8000"; // or your deployed URL

export const registerUser = (data) => axios.post(`${BASE_URL}/register`, data);
export const loginUser = (data) => axios.post(`${BASE_URL}/login`, data);
