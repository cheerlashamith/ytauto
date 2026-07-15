import { Search, Bell, Sun, Moon } from 'lucide-react';
import { useState, useEffect } from 'react';
import './Navbar.css';

export default function Navbar() {
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <header className="navbar">
      <div className="search-bar">
        <Search size={18} className="search-icon" />
        <input type="text" placeholder="Search (Cmd + K)" />
      </div>
      
      <div className="navbar-actions">
        <button className="icon-btn" onClick={toggleTheme}>
          {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
        </button>
        <button className="icon-btn notification-btn">
          <Bell size={20} />
          <span className="badge"></span>
        </button>
      </div>
    </header>
  );
}
