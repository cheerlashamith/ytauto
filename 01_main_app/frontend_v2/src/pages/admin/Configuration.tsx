import { useState, useEffect } from 'react';
import { Save, Key, Video } from 'lucide-react';
import './Configuration.css';

export default function Configuration() {
  const [config, setConfig] = useState<any>(null);
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/config')
      .then(res => res.json())
      .then(data => {
        setConfig(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch config", err);
        setLoading(false);
      });
  }, []);

  const handleSave = async () => {
    setSaving(true);
    try {
      await fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config)
      });
      alert('Configuration saved successfully!');
    } catch (err) {
      alert('Failed to save configuration');
    }
    setSaving(false);
  };

  const handleChange = (section: string, key: string, value: any) => {
    setConfig((prev: any) => ({
      ...prev,
      [section]: {
        ...prev[section],
        [key]: value
      }
    }));
  };

  if (loading) return <div style={{padding: '2rem'}}>Loading configuration...</div>;

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>System Configuration</h1>
          <p className="text-muted">Manage global settings, API keys, and system parameters.</p>
        </div>
        <button className="btn btn-primary" onClick={handleSave} disabled={saving}>
          <Save size={18} />
          {saving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>

      <div className="settings-layout" style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '2rem' }}>
        
        {/* Providers Section */}
        <div className="card glass-panel" style={{ padding: '2rem' }}>
          <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem', fontSize: '1.25rem' }}>
            <Key size={20} />
            API Keys & Providers
          </h2>
          
          <div className="form-group" style={{ marginBottom: '1rem' }}>
            <label>Pexels API Key</label>
            <input 
              type="password" 
              className="form-control" 
              value={config?.providers?.pexels_api_key || ''} 
              onChange={e => handleChange('providers', 'pexels_api_key', e.target.value)}
              placeholder="Enter your Pexels API Key for B-Roll..."
            />
            <p className="text-muted" style={{ fontSize: '0.85rem', marginTop: '0.25rem' }}>Required for Autonomous and YouTube generation modes.</p>
          </div>

          <div className="form-group" style={{ marginBottom: '1rem' }}>
            <label>Ollama URL</label>
            <input 
              type="text" 
              className="form-control" 
              value={config?.providers?.ollama_url || 'http://127.0.0.1:11434'} 
              onChange={e => handleChange('providers', 'ollama_url', e.target.value)}
            />
          </div>
          
          <div className="form-group" style={{ marginBottom: '1rem' }}>
            <label>Planner Model (Ollama)</label>
            <input 
              type="text" 
              className="form-control" 
              value={config?.providers?.planner_model || ''} 
              onChange={e => handleChange('providers', 'planner_model', e.target.value)}
            />
          </div>
        </div>

        {/* Rendering Section */}
        <div className="card glass-panel" style={{ padding: '2rem' }}>
          <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem', fontSize: '1.25rem' }}>
            <Video size={20} />
            Rendering Defaults
          </h2>
          
          <div className="form-group" style={{ marginBottom: '1rem' }}>
            <label>Story Video Aspect Ratio</label>
            <select 
              className="form-control" 
              value={config?.rendering?.story_aspect || '9:16'}
              onChange={e => handleChange('rendering', 'story_aspect', e.target.value)}
            >
              <option value="9:16">9:16 (Shorts/TikTok)</option>
              <option value="16:9">16:9 (YouTube Standard)</option>
            </select>
          </div>

          <div className="form-group" style={{ marginBottom: '1rem' }}>
            <label>Course Video Aspect Ratio</label>
            <select 
              className="form-control" 
              value={config?.rendering?.course_aspect || '16:9'}
              onChange={e => handleChange('rendering', 'course_aspect', e.target.value)}
            >
              <option value="16:9">16:9 (YouTube Standard)</option>
              <option value="9:16">9:16 (Shorts/TikTok)</option>
            </select>
          </div>
          
          <div className="form-group" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '1.5rem' }}>
            <input 
              type="checkbox" 
              checked={config?.rendering?.subtitle_enabled ?? true}
              onChange={e => handleChange('rendering', 'subtitle_enabled', e.target.checked)}
              style={{ width: 'auto' }}
            />
            <label style={{ margin: 0 }}>Enable Subtitles by Default</label>
          </div>
        </div>

      </div>
    </div>
  );
}
