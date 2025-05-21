import { Link, useLocation } from 'react-router-dom';
import { useState } from 'react';

function PatientLayout({ children }) {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <div className="flex h-screen w-screen overflow-hidden">
      {/* Sidebar */}
      <aside
        className={`flex-shrink-0 h-full overflow-y-auto bg-white text-gray-700 shadow-lg transition-all duration-300 ${
          collapsed ? 'w-16' : 'w-64'
        }`}
      >
        <div className="flex items-center justify-between px-4 py-3">
          {/* Logo or Title */}
          {!collapsed && <h2 className="text-lg font-bold">Dashboard</h2>}
          {/* Toggle Button */}
          <button onClick={() => setCollapsed(!collapsed)} className="text-xl text-gray-700">
            ☰
          </button>
        </div>

        {/* Navigation */}
        <nav className="px-4 space-y-6 text-sm">
          {/* Appointments Section */}
          <div className="space-y-4">
            <h3 className={`text-gray-600 ${collapsed && 'hidden'}`}>My Health</h3>
            <ul className="space-y-2">
              <li>
                <Link
                  to="/medical-records"
                  className={`block px-3 py-2 rounded transition ${
                    isActive('/medical-records') ? 'bg-blue-500 text-white' : 'text-gray-700 hover:bg-blue-50'
                  }`}
                >
                  {collapsed ? '📂' : 'Medical Records'}
                </Link>
              </li>
              <li>
                <Link
                  to="/prescriptions"
                  className={`block px-3 py-2 rounded transition ${
                    isActive('/prescriptions') ? 'bg-blue-500 text-white' : 'text-gray-700 hover:bg-blue-50'
                  }`}
                >
                  {collapsed ? '💊' : 'Prescriptions'}
                </Link>
              </li>
            </ul>
          </div>

          {/* Chat Section */}
          <div className="space-y-4">
            <h3 className={`text-gray-600 ${collapsed && 'hidden'}`}>Contact</h3>
            <ul className="space-y-2">
              <li>
                <Link
                  to="/chatbot"
                  className={`block px-3 py-2 rounded transition ${
                    isActive('/chat') ? 'bg-blue-500 text-white' : 'text-gray-700 hover:bg-blue-50'
                  }`}
                >
                  {collapsed ? '🤖' : 'Chat with Doctor'}
                </Link>
              </li>
            </ul>
          </div>
        </nav>
      </aside>

      {/* Main Content */}
      <div className="flex flex-col flex-1 h-full overflow-auto">
        <main className="flex-1 w-full px-6 py-8 overflow-auto">{children}</main>
      </div>
    </div>
  );
}

export default PatientLayout;