import { Outlet, Link } from 'react-router-dom';
import './patient.css';

function DashboardLayout() {
    return (
        <div className="dashboard-layout">
            <aside className="sidebar">
                <h2><Link to="/patient/dashboard">Dashboard</Link></h2>
                <ul>
                    <li><Link to="/patient/profile">Profile</Link></li>
                    <li><Link to="/patient/predict">Predict HbA1c</Link></li>
                    <li><Link to="/patient/chatbot">Chatbot</Link></li>
                    <li><Link to="/patient/logout">Logout</Link></li>
                </ul>
            </aside>
            <main className="content">
                <Outlet />
            </main>
        </div>
    );
}

export default DashboardLayout;
