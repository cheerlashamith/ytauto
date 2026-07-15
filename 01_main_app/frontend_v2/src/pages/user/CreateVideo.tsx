import { useState, useEffect } from 'react';
import { Sparkles, MonitorPlay, Wand2, User, Play, Loader2, Clock } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import './CreateVideo.css';

export default function CreateVideo() {
  const navigate = useNavigate();
  const [mode, setMode] = useState('manual');
  const [loading, setLoading] = useState(false);
  const [topic, setTopic] = useState('');
  
  const [visualStyle, setVisualStyle] = useState('manim_course');
  const [voice, setVoice] = useState('en-US-AndrewMultilingualNeural');
  const [aspect, setAspect] = useState('16:9');

  // Auto-update selections when mode changes
  useEffect(() => {
    if (mode === 'manual') {
      setVisualStyle('manim_course');
      setAspect('16:9');
      setVoice('en-US-AndrewMultilingualNeural');
    } else if (mode === 'story') {
      setVisualStyle('comfyui_story');
      setAspect('9:16');
      setVoice('en-US-JennyNeural');
    } else if (mode === 'youtube') {
      setVisualStyle('pexels');
      setAspect('16:9');
      setVoice('en-US-AndrewMultilingualNeural');
    } else if (mode === 'autonomous') {
      setVisualStyle('pexels');
      setAspect('16:9');
      setVoice('en-US-AndrewMultilingualNeural');
    }
  }, [mode]);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await fetch('/api/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mode: mode === 'manual' ? 'manual_course' : mode,
          topic: topic,
          youtube_url: mode === 'youtube' ? topic : undefined,
          visual_style: visualStyle,
          aspect: aspect,
          voice: voice
        })
      });
      
      const data = await response.json();
      setLoading(false);
      
      if (data.job_id) {
        navigate(`/user/progress?jobId=${data.job_id}`);
      } else {
        alert('Failed to start job: ' + JSON.stringify(data));
      }
    } catch (err) {
      setLoading(false);
      alert('Network error submitting job');
    }
  };

  return (
    <div className="create-page">
      <div className="create-header">
        <h1>Create Video</h1>
        <p className="text-muted">Select a mode and enter your topic to start the AI generation pipeline.</p>
      </div>

      <div className="mode-selector">
        <div className={`mode-card ${mode === 'manual' ? 'active' : ''}`} onClick={() => setMode('manual')}>
          <User className="mode-icon text-primary" />
          <div className="mode-info">
            <h3>Manual Course</h3>
            <p>Syllabus-aware generation</p>
          </div>
        </div>
        <div className={`mode-card ${mode === 'story' ? 'active' : ''}`} onClick={() => setMode('story')}>
          <Wand2 className="mode-icon text-purple" />
          <div className="mode-info">
            <h3>Story Mode</h3>
            <p>ComfyUI visual narrative</p>
          </div>
        </div>
        <div className={`mode-card ${mode === 'youtube' ? 'active' : ''}`} onClick={() => setMode('youtube')}>
          <MonitorPlay className="mode-icon text-danger" />
          <div className="mode-info">
            <h3>YouTube Extract</h3>
            <p>URL to course conversion</p>
          </div>
        </div>
        <div className={`mode-card ${mode === 'autonomous' ? 'active' : ''}`} onClick={() => setMode('autonomous')}>
          <Sparkles className="mode-icon text-success" />
          <div className="mode-info">
            <h3>Autonomous</h3>
            <p>AI selects everything</p>
          </div>
        </div>
      </div>

      <form className="create-form card glass-panel" onSubmit={handleGenerate}>
        <div className="form-group">
          <label htmlFor="topic">{mode === 'youtube' ? 'YouTube URL' : 'Topic / Prompt'}</label>
          <input
            type="text"
            className="input-field"
            required={mode !== 'manual'}
            placeholder={
              mode === 'manual' ? 'Enter your topic here... (leave empty for batch syllabus mode)' :
              mode === 'story' ? 'Enter your story topic here... (e.g. A brave little toaster)' :
              mode === 'youtube' ? 'Enter your YouTube URL here... (e.g. https://youtube.com/watch?v=...)' :
              'Enter your topic here...'
            }
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />
        </div>

        <div className="form-row">
          <div className="form-group flex-1">
            <label>Visual Style</label>
            <select className="input-field" value={visualStyle} onChange={e => setVisualStyle(e.target.value)}>
              <option value="manim_course">Manim Course (Code & Math)</option>
              <option value="comfyui_story">ComfyUI Story (Narrative)</option>
              <option value="pexels">Pexels Stock (Documentary)</option>
            </select>
          </div>
          
          <div className="form-group flex-1">
            <label>Voice Provider</label>
            <select className="input-field" value={voice} onChange={e => setVoice(e.target.value)}>
              <option value="en-US-AndrewMultilingualNeural">Edge TTS - Andrew (Male)</option>
              <option value="en-US-JennyNeural">Edge TTS - Jenny (Female)</option>
            </select>
          </div>

          <div className="form-group flex-1">
            <label>Aspect Ratio</label>
            <select className="input-field" value={aspect} onChange={e => setAspect(e.target.value)}>
              <option value="16:9">16:9 (Landscape)</option>
              <option value="9:16">9:16 (Portrait / Shorts)</option>
              <option value="1:1">1:1 (Square)</option>
            </select>
          </div>
        </div>

        <div className="form-footer">
          <div className="estimated-time">
            <Clock size={16} className="text-muted" />
            <span className="text-sm text-muted">Estimated time: ~3 mins per scene</span>
          </div>
          <button type="submit" className="btn btn-primary generate-btn" disabled={loading}>
            {loading ? (
              <>
                <Loader2 size={18} className="animate-spin" />
                Initializing Pipeline...
              </>
            ) : (
              <>
                <Play size={18} />
                Generate Video
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
