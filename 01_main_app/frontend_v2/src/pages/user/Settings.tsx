import { Save, User, Globe, Shield, Bell } from 'lucide-react';
import './Settings.css';

export default function Settings() {
  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Settings</h1>
          <p className="text-muted">Manage your account preferences and API keys.</p>
        </div>
        <button className="btn btn-primary">
          <Save size={18} />
          Save Changes
        </button>
      </div>

      <div className="settings-layout">
        <div className="settings-sidebar">
          <button className="settings-tab active"><User size={18} /> Profile</button>
          <button className="settings-tab"><Globe size={18} /> Preferences</button>
          <button className="settings-tab"><Shield size={18} /> API Keys</button>
          <button className="settings-tab"><Bell size={18} /> Notifications</button>
        </div>
        
        <div className="settings-content">
          <div className="card glass-panel">
            <h2 className="card-title">Profile Settings</h2>
            
            <div className="form-group">
              <label>Display Name</label>
              <input type="text" className="input-field" defaultValue="Demo User" />
            </div>

            <div className="form-group">
              <label>Email Address</label>
              <input type="email" className="input-field" defaultValue="demo@autocourse.ai" />
            </div>

            <div className="form-group">
              <label>Avatar Background Color</label>
              <div className="color-picker-mock">
                <div className="color-swatch" style={{backgroundColor: 'var(--primary-color)'}}></div>
                <div className="color-swatch" style={{backgroundColor: 'var(--accent-purple)'}}></div>
                <div className="color-swatch" style={{backgroundColor: 'var(--success-color)'}}></div>
                <div className="color-swatch" style={{backgroundColor: 'var(--danger-color)'}}></div>
                <div className="color-swatch" style={{backgroundColor: 'var(--warning-color)'}}></div>
              </div>
            </div>
          </div>

          <div className="card glass-panel mt-4">
            <h2 className="card-title">Default Generation Preferences</h2>
            
            <div className="form-group">
              <label>Default Resolution</label>
              <select className="input-field">
                <option>1080p (1920x1080)</option>
                <option>4K (3840x2160)</option>
                <option>Vertical (1080x1920)</option>
              </select>
            </div>

            <div className="form-group">
              <label>Default AI Voice</label>
              <select className="input-field">
                <option>Nova (Female, Professional)</option>
                <option>Onyx (Male, Deep)</option>
                <option>Alloy (Neutral)</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
