import { useState, useEffect } from 'react';
import { Activity, Cpu, Server, Zap } from 'lucide-react';
import './SystemDashboard.css';

export default function SystemDashboard() {
  const [metrics, setMetrics] = useState<any>(null);
  const [plugins, setPlugins] = useState<any[]>([]);
  const [history, setHistory] = useState<number[]>([]);

  useEffect(() => {
    const fetchMetrics = () => {
      fetch('/api/admin/metrics').then(r => r.json()).then(data => {
        setMetrics(data);
        setHistory(prev => {
          const next = [...prev, data.cpu_percent];
          if (next.length > 20) return next.slice(next.length - 20);
          return next;
        });
      }).catch(console.error);
    };

    const fetchPlugins = () => {
      fetch('/api/admin/plugins').then(r => r.json()).then(setPlugins).catch(console.error);
    };

    fetchMetrics();
    fetchPlugins();
    
    const interval = setInterval(fetchMetrics, 3000); // Poll metrics every 3s
    return () => clearInterval(interval);
  }, []);

  const cpu = metrics?.cpu_percent || 0;
  const ramPercent = metrics?.ram_percent || 0;
  const ramGb = metrics?.ram_used_gb || 0;
  const workers = metrics?.active_workers || 0;
  const queued = metrics?.queued_jobs || 0;

  // Pad history to 20 for graph
  const displayHistory = [...history];
  while (displayHistory.length < 20) {
    displayHistory.unshift(0);
  }

  return (
    <div className="admin-page">
      <div className="page-header">
        <div>
          <h1>System Dashboard</h1>
          <p className="text-muted">Real-time infrastructure health and worker metrics.</p>
        </div>
        <div className="system-status-indicator">
          <span className="pulsing-dot green"></span>
          All Systems Operational
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card admin-stat">
          <div className="stat-icon bg-blue-100">
            <Cpu className="text-primary" size={24} />
          </div>
          <div className="stat-content">
            <span className="stat-value">{cpu.toFixed(1)}%</span>
            <span className="stat-label">CPU Usage</span>
          </div>
          <div className="progress-bar-mini">
            <div className="progress-fill bg-primary" style={{width: `${cpu}%`}}></div>
          </div>
        </div>
        <div className="stat-card admin-stat">
          <div className="stat-icon bg-purple-100">
            <Server className="text-purple" size={24} />
          </div>
          <div className="stat-content">
            <span className="stat-value">{ramGb.toFixed(1)} GB</span>
            <span className="stat-label">RAM Usage ({ramPercent}%)</span>
          </div>
          <div className="progress-bar-mini">
            <div className="progress-fill bg-purple" style={{width: `${ramPercent}%`}}></div>
          </div>
        </div>
        <div className="stat-card admin-stat">
          <div className="stat-icon bg-green-100">
            <Zap className="text-success" size={24} />
          </div>
          <div className="stat-content">
            <span className="stat-value">{workers}</span>
            <span className="stat-label">Active Workers</span>
          </div>
          <div className="progress-bar-mini">
            <div className="progress-fill bg-success" style={{width: `${Math.min(100, workers * 25)}%`}}></div>
          </div>
        </div>
        <div className="stat-card admin-stat">
          <div className="stat-icon bg-orange-100">
            <Activity className="text-warning" size={24} />
          </div>
          <div className="stat-content">
            <span className="stat-value">{queued}</span>
            <span className="stat-label">Queued Jobs</span>
          </div>
        </div>
      </div>

      <div className="admin-grid">
        <div className="card glass-panel">
          <h2 className="card-title">Live CPU Utilization</h2>
          <div className="mock-graph">
            <div className="bars">
              {displayHistory.map((h, i) => (
                <div key={i} className="bar-wrapper">
                  <div className="bar" style={{height: `${Math.max(2, h)}%`}}></div>
                </div>
              ))}
            </div>
            <div className="graph-labels">
              <span>-60s</span>
              <span>-30s</span>
              <span>Now</span>
            </div>
          </div>
        </div>

        <div className="card glass-panel">
          <h2 className="card-title">Active Models</h2>
          <table className="admin-table">
            <thead>
              <tr>
                <th>Model Name</th>
                <th>Provider</th>
                <th>Status</th>
                <th>VRAM (Est)</th>
              </tr>
            </thead>
            <tbody>
              {plugins.length === 0 && <tr><td colSpan={4}>Loading plugins...</td></tr>}
              {plugins.map(p => (
                <tr key={p.plugin}>
                  <td>{p.model}</td>
                  <td style={{textTransform: 'capitalize'}}>{p.plugin}</td>
                  <td>
                    {p.healthy ? 
                      <span className="status-badge active">Loaded</span> : 
                      <span className="status-badge offline">Unloaded</span>
                    }
                  </td>
                  <td>{p.healthy ? 'Auto' : '0 GB'}</td>
                </tr>
              ))}
              <tr>
                <td>SDXL 1.0 / FLUX</td>
                <td>ComfyUI</td>
                <td><span className="status-badge active">Loaded</span></td>
                <td>External</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
