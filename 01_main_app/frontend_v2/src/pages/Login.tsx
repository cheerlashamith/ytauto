import { useNavigate } from 'react-router-dom';
import { User, ShieldCheck, Sparkles } from 'lucide-react';
import './Login.css';

export default function Login() {
  const navigate = useNavigate();

  const handleLogin = (role: 'user' | 'admin') => {
    localStorage.setItem('role', role);
    if (role === 'admin') {
      navigate('/admin/system');
    } else {
      navigate('/user/dashboard');
    }
  };

  return (
    <div className="login-container">
      <div className="login-card glass-panel">
        <div className="login-header">
          <div className="logo-icon-large">
            <Sparkles size={32} color="white" />
          </div>
          <h1>AutoCourse Studio</h1>
          <p className="text-muted">Select a demo account to continue</p>
        </div>

        <div className="login-options">
          <button className="login-btn user-btn" onClick={() => handleLogin('user')}>
            <div className="btn-icon">
              <User size={24} />
            </div>
            <div className="btn-text">
              <h3>Demo User</h3>
              <p>Create and manage videos</p>
            </div>
          </button>

          <button className="login-btn admin-btn" onClick={() => handleLogin('admin')}>
            <div className="btn-icon">
              <ShieldCheck size={24} />
            </div>
            <div className="btn-text">
              <h3>Demo Admin</h3>
              <p>System health and config</p>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
}
