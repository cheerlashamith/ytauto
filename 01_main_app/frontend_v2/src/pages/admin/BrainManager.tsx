import { useState, useEffect } from 'react';
import { Brain, Server, CheckCircle2, AlertCircle } from 'lucide-react';

export default function BrainManager() {
  const [config, setConfig] = useState<any>(null);
  const [plugins, setPlugins] = useState<any[]>([]);

  useEffect(() => {
    fetch('/api/config').then(r => r.json()).then(setConfig).catch(console.error);
    fetch('/api/admin/plugins').then(r => r.json()).then(setPlugins).catch(console.error);
  }, []);

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Brain Manager</h1>
          <p className="text-muted">Manage active AI models and router configurations.</p>
        </div>
      </div>
      
      <div className="admin-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        <div className="card glass-panel">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
            <Brain className="text-primary" />
            <h2 className="card-title" style={{ margin: 0 }}>Active LLMs</h2>
          </div>
          {plugins.length === 0 ? <p className="text-muted">Loading models...</p> : plugins.map(p => (
            <div key={p.plugin} style={{ padding: '1rem', background: 'var(--bg-color)', borderRadius: '8px', marginBottom: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <strong>{p.model}</strong>
                {p.healthy ? 
                  <span className="status-badge success"><CheckCircle2 size={12}/> Ready</span> :
                  <span className="status-badge offline"><AlertCircle size={12}/> Error</span>
                }
              </div>
              <p className="text-muted" style={{ fontSize: '0.85rem' }}>Tasks: {p.task_types?.join(', ') || 'Various'}</p>
            </div>
          ))}
        </div>

        <div className="card glass-panel">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
            <Server className="text-purple" />
            <h2 className="card-title" style={{ margin: 0 }}>System Config</h2>
          </div>
          {config ? (
            <div style={{ padding: '1rem', background: 'var(--bg-color)', borderRadius: '8px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <strong>Planner Model</strong>
                <span>{config.providers?.planner_model}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <strong>Max Workers</strong>
                <span>{config.brain_manager?.max_parallel_workers}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <strong>Job Timeout</strong>
                <span>{config.brain_manager?.timeout_seconds}s</span>
              </div>
            </div>
          ) : <p className="text-muted">Loading config...</p>}
        </div>
      </div>
    </div>
  );
}
