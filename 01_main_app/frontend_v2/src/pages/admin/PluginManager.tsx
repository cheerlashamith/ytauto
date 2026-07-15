import { useState, useEffect } from 'react';
import { ToggleRight, ToggleLeft, RefreshCcw } from 'lucide-react';

interface PluginHealth {
  plugin: string;
  healthy: boolean;
  model: string;
  task_types: string[];
  metrics: {
    total_calls: number;
    failures: number;
    avg_response_time: number;
  };
}

export default function PluginManager() {
  const [plugins, setPlugins] = useState<PluginHealth[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchPlugins = () => {
    setLoading(true);
    fetch('/api/admin/plugins')
      .then(res => res.json())
      .then(data => {
        setPlugins(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch plugins", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchPlugins();
  }, []);

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Plugin Manager</h1>
          <p className="text-muted">Manage AI engines, renderers, and external integrations.</p>
        </div>
        <button className="btn btn-secondary" onClick={fetchPlugins}>
          <RefreshCcw size={18} />
          Refresh
        </button>
      </div>

      <div className="card glass-panel">
        <table className="history-table">
          <thead>
            <tr>
              <th>Plugin / Model</th>
              <th>Status</th>
              <th>Supported Tasks</th>
              <th>Calls / Fails</th>
              <th>Avg Latency</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={6} style={{textAlign: 'center', padding: '2rem'}}>Loading plugins...</td></tr>
            ) : plugins.length === 0 ? (
              <tr><td colSpan={6} style={{textAlign: 'center', padding: '2rem'}}>No plugins registered.</td></tr>
            ) : plugins.map(p => (
              <tr key={p.plugin}>
                <td>
                  <strong>{p.plugin}</strong><br/>
                  <span className="text-muted" style={{fontSize: '0.8rem'}}>{p.model}</span>
                </td>
                <td>
                  {p.healthy ? (
                    <span className="status-badge success">Healthy</span>
                  ) : (
                    <span className="status-badge danger">Failing</span>
                  )}
                </td>
                <td style={{fontSize: '0.85rem'}}>{p.task_types.join(', ')}</td>
                <td>{p.metrics.total_calls} / {p.metrics.failures}</td>
                <td>{p.metrics.avg_response_time > 0 ? `${p.metrics.avg_response_time.toFixed(2)}s` : 'N/A'}</td>
                <td>
                  <button className="icon-btn" title="Toggle">
                    {p.healthy ? <ToggleRight size={20} className="text-success" /> : <ToggleLeft size={20} className="text-muted" />}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
