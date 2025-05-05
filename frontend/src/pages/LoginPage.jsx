import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/login', {
        email,
        password
      });
      const { role } = res.data;
      if (role === 'doctor') navigate('/doctor/dashboard');
      else if (role === 'patient') navigate('/patient/dashboard');
    } catch (err) {
      alert('Login failed. Check credentials.');
    }
  };

  return (
    <div>
      <h2>Login</h2>
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
      <button onClick={handleLogin}>Login</button>
      <p>Don't have an account? <a href="/register">Register here</a></p>
    </div>
  );
}

export default LoginPage;
