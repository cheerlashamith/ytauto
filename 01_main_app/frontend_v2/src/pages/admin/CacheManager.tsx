import { useState, useEffect } from 'react';
import { Trash2, HardDrive } from 'lucide-react';

export default function CacheManager() {
  const [cacheStats, setCacheStats] = useState<any>(null);

  useEffect(() => {
    fetch('/api/admin/cache').then(r => r.json()).then(setCacheStats).catch(console.error);
  }, []);

  const totalBytes = cacheStats?.total_size_bytes || 0;
  const totalFiles = cacheStats?.total_files || 0;
  const mb = (totalBytes / (1024 * 1024)).toFixed(2);

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Cache Manager</h1>
          <p className="text-muted">Manage disk usage, temp files, and model weights cache.</p>
        </div>
      </div>
      
      <div className="admin-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        <div className="card glass-panel">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
            <HardDrive className="text-primary" />
            <h2 className="card-title" style={{ margin: 0 }}>AI Inference Cache</h2>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: '4px' }}>
                <span>Total Cache Size</span>
                <strong>{mb} MB ({totalFiles} files)</strong>
              </div>
              <div className="progress-bar" style={{ height: '6px', background: 'var(--border-color)', borderRadius: '3px' }}>
                <div style={{ height: '100%', width: `${Math.min(100, (totalBytes / (100 * 1024 * 1024)) * 100)}%`, background: 'var(--primary-color)', borderRadius: '3px' }}></div>
              </div>
            </div>
            {cacheStats?.tasks && Object.entries(cacheStats.tasks).map(([task, data]: [string, any]) => (
              <div key={task}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: '4px' }}>
                  <span style={{textTransform: 'capitalize'}}>{task} Cache</span>
                  <strong>{(data.size_bytes / 1024).toFixed(1)} KB</strong>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="card glass-panel">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
            <Trash2 className="text-danger" />
            <h2 className="card-title" style={{ margin: 0 }}>Cleanup Actions</h2>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <button className="btn btn-secondary" style={{ width: '100%', justifyContent: 'center' }}>
              Clear Render Temp Files
            </button>
            <button className="btn btn-secondary" style={{ width: '100%', justifyContent: 'center' }} onClick={() => alert('Feature coming soon')}>
              Clear Audio Cache
            </button>
            <button className="btn btn-secondary" style={{ width: '100%', justifyContent: 'center', borderColor: 'var(--danger-color)', color: 'var(--danger-color)' }} onClick={() => alert('Feature coming soon')}>
              Purge All AI Cache
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
