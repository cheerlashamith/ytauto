import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import './AppLayout.css';

export default function AppLayout() {
  return (
    <div className="app-container">
      <Sidebar />
      <div className="main-content">
        <Navbar />
        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
