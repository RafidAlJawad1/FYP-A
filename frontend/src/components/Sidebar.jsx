import { Link } from 'react-router-dom';

export default function Sidebar() {
  return (
    <div className="sidebar">
      <h3>Patient Menu</h3>
      <ul>
        <li><Link to="profile">Profile</Link></li>
        <li><Link to="predict">Predict HbA1C</Link></li>
        <li><Link to="chatbot">Chatbot</Link></li>
        <li><Link to="/login">Logout</Link></li>
      </ul>
    </div>
  );
}