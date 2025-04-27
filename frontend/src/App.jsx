import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './Layout';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import RiskPredictionForm from './RiskPredictionForm';
import './App.css';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/patients" element={<Profile />} />
          <Route path="/patients/create" element={<Profile />} />
          <Route path="/patients/add-from-app" element={<Profile />} />
          <Route path="/predict" element={<RiskPredictionForm />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
