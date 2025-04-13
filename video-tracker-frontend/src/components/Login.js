import React, { useState } from 'react';
import { loginUser, registerUser } from '../api/auth';

function Login({ onLogin }) {
    const [form, setForm] = useState({ username: '', password: '' });

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleLogin = async () => {
        const res = await loginUser(form);
        localStorage.setItem("token", res.data.access_token);
        onLogin();
    };

    const handleRegister = async () => {
        await registerUser(form);
        alert("User registered. You can now log in.");
    };

    return (
        <div>
            <h2>Login or Register</h2>
            <input name="username" onChange={handleChange} placeholder="Username" />
            <input name="password" type="password" onChange={handleChange} placeholder="Password" />
            <button onClick={handleLogin}>Login</button>
            <button onClick={handleRegister}>Register</button>
        </div>
    );
}

export default Login;
