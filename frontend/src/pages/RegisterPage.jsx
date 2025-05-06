import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function RegisterPage() {
    const navigate = useNavigate();
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('patient');

    const handleRegister = async () => {
        try {
            const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/register`, {
                name,
                email,
                password,
                role,
            });
            const { user } = response.data;
            localStorage.setItem('user', JSON.stringify(user));
            alert('Registration success.');
            navigate('/login');
        } catch (err) {
            alert('Registration failed.');
        }
    };

    return (
        <div className="auth-page">
            <div className="auth-card">
                <h2>Register</h2>
                <input
                    type="text"
                    placeholder="Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <select value={role} onChange={(e) => setRole(e.target.value)}>
                    <option value="patient">Patient</option>
                    <option value="doctor">Doctor</option>
                </select>
                <button onClick={handleRegister}>Register</button>
                <p>Already have an account? <a href="/login">Login here</a></p>
            </div>
        </div>
    );
}

export default RegisterPage;
