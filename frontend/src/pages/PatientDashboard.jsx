import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './patient/patient.css';

function PatientDashboard() {
  const [user, setUser] = useState({ name: 'patient' });
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  return (
    <div className="patient-dashboard centered">
      <h1>Welcome back, {user.name}!</h1>
      <p>Your personal health dashboard is ready.</p>
      <div className="dashboard-buttons">
        <button onClick={() => navigate('/patient/profile')}>Profile Page</button>
        <button onClick={() => navigate('/patient/predict')}>Predict HbA1c</button>
        <button onClick={() => navigate('/patient/chatbot')}>Chatbot</button>
        <button onClick={() => navigate('/patient/logout')} className="logout-btn">Logout</button>
      </div>
    </div>
  );
}

export default PatientDashboard;
