import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AdminLayout from './AdminLayout';
import PatientLayout from './PatientLayout';
import Layout from './Layout';
import Dashboard from './pages/Dashboard';
import PatientsList from './pages/PatientsList';
import PatientProfile from './pages/PatientProfile';
import RiskDashboard from './pages/RiskDashboard';
import RiskPredictionForm from './pages/RiskPredictionForm';
import CreatePatient from './pages/CreatePatient'; 
import TherapyDashboard from './pages/TherapyDashboard'; 
import TherapyEffectivenessForm from './pages/TherapyEffectivenessForm';
import TreatmentRecommendationDashboard from './pages/TreatmentRecommendationDashboard.jsx';
import TreatmentRecommendationForm from './pages/TreatmentRecommendationForm';
import SignIn from './pages/SignIn';
import RegistrationForm from './pages/RegistrationForm';
import './App.css';

function App() {
  return (
    <Router>
     <AdminLayout>
        <Routes>
          <Route path="/signin" element={<SignIn/>} />
          <Route path="/" element={<Dashboard />} />
          <Route path="/patients" element={<PatientsList />} />

          {/* Parent route with nested routes */}
          <Route path="/patient/:id/*" element={<PatientProfile />} />

          <Route path="/predict" element={<RiskDashboard />} />
          <Route path="/predict/:id" element={<RiskPredictionForm />} />

          {/* Route for TherapyEffectivenessForm */}
          <Route path="/therapy-effectiveness" element={<TherapyDashboard />} />
          <Route path="/therapy-effectiveness/:id" element={<TherapyEffectivenessForm />} />

          {/* Route for TreatmentRecommendationForm */}
          <Route path="/treatment-recommendation" element={<TreatmentRecommendationDashboard />} />
          <Route path="/treatment-recommendation/:id" element={<TreatmentRecommendationForm />} />

          {/* Route for CreatePatient */}
          <Route path="/patients/create" element={<CreatePatient />} />

          {/* Route for RegistrationForm */}
          <Route path="/register" element={<RegistrationForm />} />
        </Routes>
      </AdminLayout>
    </Router>
  );
}

export default App;
