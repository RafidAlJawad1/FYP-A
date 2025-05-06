import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import RegisterPage from './pages/RegisterPage';
import LoginPage from './pages/LoginPage';

import PatientDashboard from './pages/PatientDashboard';
import DashboardLayout from './pages/patient/DashboardLayout';
import ProfilePage from './pages/patient/ProfilePage';
import PredictHba1c from './pages/patient/PredictHba1c';
import Chatbot from './pages/patient/Chatbot';
import Logout from './pages/patient/Logout';

import DoctorDashboard from './pages/DoctorDashboard';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/patient/dashboard" element={<PatientDashboard />} />

        <Route path="/patient" element={<DashboardLayout />}>
          <Route path="profile" element={<ProfilePage />} />
          <Route path="predict" element={<PredictHba1c />} />
          <Route path="chatbot" element={<Chatbot />} />
          <Route path="logout" element={<Logout />} />
        </Route>

        {/* Doctor side routes */}
        <Route path="/doctor/dashboard" element={<DoctorDashboard />} />
     
      </Routes>
    </Router>
  );
}

export default App;

