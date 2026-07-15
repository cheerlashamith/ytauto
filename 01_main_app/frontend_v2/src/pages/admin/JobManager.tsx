import { useState, useEffect } from 'react';
import { Play, Square, RefreshCcw } from 'lucide-react';

interface JobSummary {
  job_id: string;
  status: string;
  request: any;
  message: string;
  progress_percentage: number;
}

export default function JobManager() {
  const [jobs, setJobs] = useState<JobSummary[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchJobs = () => {
    setLoading(true);
    fetch('/api/jobs')
      .then(res => res.json())
      .then(data => {
        const arr = Object.values(data) as JobSummary[];
        arr.reverse();
        setJobs(arr);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch jobs", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Job Manager</h1>
          <p className="text-muted">Monitor and control system background tasks.</p>
        </div>
        <button className="btn btn-secondary" onClick={fetchJobs}>
          <RefreshCcw size={18} />
          Refresh
        </button>
      </div>

      <div className="card glass-panel">
        <table className="history-table">
          <thead>
            <tr>
              <th>Job ID</th>
              <th>Task Details</th>
              <th>Status</th>
              <th>Progress</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={5} style={{textAlign: 'center', padding: '2rem'}}>Loading jobs...</td></tr>
            ) : jobs.length === 0 ? (
              <tr><td colSpan={5} style={{textAlign: 'center', padding: '2rem'}}>No active jobs.</td></tr>
            ) : jobs.map(job => (
              <tr key={job.job_id}>
                <td className="job-id">{job.job_id.substring(0, 8)}...</td>
                <td>{job.request?.topic || job.request?.youtube_url || "AutoCourse Task"}</td>
                <td>
                  <span className={`status-badge ${job.status === 'completed' ? 'success' : job.status === 'failed' ? 'danger' : ''}`}>
                    {job.status}
                  </span>
                </td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <div style={{ flex: 1, height: '6px', background: 'var(--border-color)', borderRadius: '3px', overflow: 'hidden' }}>
                      <div style={{ width: `${job.progress_percentage || 0}%`, height: '100%', background: 'var(--primary-color)' }}></div>
                    </div>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{job.progress_percentage || 0}%</span>
                  </div>
                </td>
                <td>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button className="icon-btn" disabled={job.status !== 'queued'} title="Start">
                      <Play size={16} />
                    </button>
                    <button className="icon-btn" disabled={job.status === 'completed' || job.status === 'failed'} title="Stop">
                      <Square size={16} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
