import { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, Users, Video } from 'lucide-react';

export default function Analytics() {
  const [totalVideos, setTotalVideos] = useState(0);
  const [successRate, setSuccessRate] = useState(0);
  const [dailyVolume, setDailyVolume] = useState<number[]>([0,0,0,0,0,0,0]);

  useEffect(() => {
    fetch('/api/jobs').then(r => r.json()).then(data => {
      const arr = Object.values(data) as any[];
      setTotalVideos(arr.length);
      const completed = arr.filter(j => j.status === 'completed').length;
      setSuccessRate(arr.length > 0 ? Math.round((completed / arr.length) * 1000) / 10 : 0);
      
      // Calculate daily volume for the last 7 days based on created_at
      const now = new Date();
      const vols = [0,0,0,0,0,0,0];
      arr.forEach(j => {
        if (!j.created_at) return;
        const d = new Date(j.created_at);
        const diffTime = Math.abs(now.getTime() - d.getTime());
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
        if (diffDays < 7) {
          vols[6 - diffDays]++;
        }
      });
      setDailyVolume(vols);
    }).catch(console.error);
  }, []);

  const maxVol = Math.max(...dailyVolume, 10); // Ensure at least 10 for scale

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>System Analytics</h1>
          <p className="text-muted">Usage statistics and performance metrics over time.</p>
        </div>
      </div>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        <div className="card glass-panel" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
            <Video size={16} /> Total Videos
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>{totalVideos}</div>
        </div>
        <div className="card glass-panel" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
            <Users size={16} /> Active Users
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>1</div>
        </div>
        <div className="card glass-panel" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
            <TrendingUp size={16} /> Success Rate
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--success-color)' }}>{successRate}%</div>
        </div>
      </div>

      <div className="card glass-panel">
        <h2 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><BarChart3 size={18} /> Generation Volume (Last 7 Days)</h2>
        <div style={{ height: '300px', display: 'flex', alignItems: 'flex-end', gap: '1rem', padding: '1rem 0', borderBottom: '1px solid var(--border-color)' }}>
          {dailyVolume.map((vol, i) => (
            <div key={i} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem' }}>
              <div style={{ width: '100%', height: `${Math.max(5, (vol/maxVol)*100)}%`, background: 'var(--primary-color)', borderRadius: '4px 4px 0 0', opacity: 0.8 }}></div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Day {i + 1}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
