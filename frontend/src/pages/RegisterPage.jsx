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
            await axios.post('http://127.0.0.1:8000/api/register', {
                name,
                email,
                password,
                role
            });
            navigate('/login');
        } catch (err) {
            alert('Registration failed.');
        }
    };

    return (
        <div>
            <h2>Register</h2>
            <input
                type="text"
                placeholder="Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
            /><br />
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            /><br />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            /><br />
            <select value={role} onChange={(e) => setRole(e.target.value)}>
                <option value="patient">Patient</option>
                <option value="doctor">Doctor</option>
            </select><br />
            <button onClick={handleRegister}>Register</button>
        </div>
    );
}

export default RegisterPage;
