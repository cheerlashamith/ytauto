import { useState, useEffect } from 'react';
import { Play, Download, MoreVertical, Search, Filter } from 'lucide-react';
import './MyVideos.css';

interface JobSummary {
  job_id: string;
  status: string;
  request: any;
  files: Record<string, any>;
}

export default function MyVideos() {
  const [jobs, setJobs] = useState<JobSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/jobs')
      .then(res => res.json())
      .then(data => {
        const arr = Object.values(data) as JobSummary[];
        // Accept jobs with either final_video or videos[0]
        const completed = arr
          .filter(j => j.status === 'completed' && (j.files?.final_video || j.files?.videos?.[0]));
        completed.reverse();
        setJobs(completed);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch jobs", err);
        setLoading(false);
      });
  }, []);

  const getVideoPath = (job: JobSummary): string => {
    return job.files?.final_video || job.files?.videos?.[0] || '';
  };

  const handleDownload = (path: string) => {
    window.open(`/api/download?path=${encodeURIComponent(path)}`, '_blank');
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>My Videos</h1>
          <p className="text-muted">Manage, view, and export your generated courses.</p>
        </div>
        <div className="header-actions">
          <div className="search-bar">
            <Search size={18} />
            <input type="text" placeholder="Search videos..." />
          </div>
          <button className="btn btn-secondary">
            <Filter size={18} />
            Filter
          </button>
        </div>
      </div>

      {loading ? (
        <div style={{padding: '2rem', textAlign: 'center'}}>Loading videos...</div>
      ) : jobs.length === 0 ? (
        <div style={{padding: '2rem', textAlign: 'center'}}>No completed videos yet.</div>
      ) : (
        <div className="video-grid">
          {jobs.map(video => (
            <div key={video.job_id} className="video-card glass-panel">
              <div className="video-thumbnail" style={{ backgroundColor: 'var(--card-bg)' }}>
                <span className="video-duration">Ready</span>
                <div className="video-play-overlay">
                  <button className="play-btn" onClick={() => handleDownload(getVideoPath(video))}>
                    <Play size={24} fill="currentColor" />
                  </button>
                </div>
              </div>
              <div className="video-details">
                <div className="video-title-row">
                  <h3 className="video-title">{video.request?.topic || video.request?.youtube_url || "AutoCourse Generation"}</h3>
                  <button className="icon-btn">
                    <MoreVertical size={16} />
                  </button>
                </div>
                <p className="video-meta">Mode: {video.request?.mode || 'auto'}</p>
                <div className="video-actions">
                  <button className="btn btn-primary btn-sm btn-block" onClick={() => handleDownload(getVideoPath(video))}>
                    <Download size={14} />
                    Export Video
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
