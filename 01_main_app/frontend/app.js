// View Elements
const landingView = document.getElementById('landing-view');
const appView = document.getElementById('app-view');
const userNav = document.getElementById('user-nav');
const adminNav = document.getElementById('admin-nav');
const roleBadge = document.getElementById('current-role-badge');
const views = document.querySelectorAll('.view');
const navButtons = document.querySelectorAll('nav button');

// Form Elements
const modeSelect = document.getElementById('mode');
const visualSelect = document.getElementById('visual');
const topicInput = document.getElementById('topic');
const topicHint = document.getElementById('topic-hint');
const youtubeGroup = document.getElementById('youtube-group');
const youtubeInput = document.getElementById('youtube');
const notesInput = document.getElementById('notes');
const submitBtn = document.getElementById('submit');
const statusBox = document.getElementById('status');

// Login / Logout Logic
document.getElementById('btn-login-user').onclick = () => login('user');
document.getElementById('btn-login-admin').onclick = () => login('admin');
document.getElementById('btn-logout').onclick = logout;

function login(role) {
  landingView.style.display = 'none';
  appView.style.display = 'grid';
  
  if (role === 'user') {
    userNav.style.display = 'flex';
    adminNav.style.display = 'none';
    roleBadge.textContent = 'Role: User';
    switchView('user-generate');
    loadJobs('user-jobs-list');
  } else {
    userNav.style.display = 'none';
    adminNav.style.display = 'flex';
    roleBadge.textContent = 'Role: Admin';
    switchView('admin-health');
    loadAdminStats();
    loadJobs('admin-jobs-list');
  }
}

function logout() {
  appView.style.display = 'none';
  landingView.style.display = 'flex';
  statusBox.classList.remove('active');
}

// Navigation Logic
navButtons.forEach(btn => {
  btn.onclick = () => {
    switchView(btn.dataset.target);
  };
});

function switchView(targetId) {
  navButtons.forEach(b => b.classList.remove('active'));
  const activeBtn = document.querySelector(`button[data-target="${targetId}"]`);
  if (activeBtn) activeBtn.classList.add('active');

  views.forEach(v => v.classList.remove('active'));
  document.getElementById(targetId).classList.add('active');
}

// Form Dynamic UI
modeSelect.onchange = () => {
  const mode = modeSelect.value;
  if (mode === 'youtube_extract') {
    youtubeGroup.style.display = 'flex';
    topicHint.textContent = 'Optional topic. The AI will primarily use the YouTube transcript.';
  } else {
    youtubeGroup.style.display = 'none';
    if (mode === 'story') {
      topicHint.textContent = 'Enter the core premise of your story.';
    } else if (mode === 'autonomous') {
      topicHint.textContent = 'Autonomous Mode: Enter ANY custom topic you want a video about.';
    } else {
      topicHint.textContent = 'Course Mode: Enter a topic to generate videos for all its subtopics.';
    }
  }
};

// API Helpers
async function postJSON(url, data) {
  const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
  return r.json();
}
async function getJSON(url) {
  const r = await fetch(url);
  return r.json();
}

function setStatus(html, type = 'info') {
  statusBox.innerHTML = html;
  statusBox.className = `status-box active ${type}`;
}

// Job Submission
submitBtn.onclick = async () => {
  submitBtn.disabled = true;
  submitBtn.textContent = 'Submitting...';
  
  const mode = modeSelect.value;
  const topic = topicInput.value.trim();
  
  let autoVisual = 'pexels';
  if (mode === 'story') autoVisual = 'comfyui_story';
  if (mode === 'manual_course') autoVisual = 'manim_course';

  const payload = {
    mode: mode,
    visual_style: autoVisual,
    topic: topic,
    youtube_url: youtubeInput.value.trim() || null,
    notes: notesInput.value.trim() || null,
  };

  if (!topic && mode !== 'manual_course' && mode !== 'autonomous') {
    setStatus('A topic is required for this mode.', 'error');
    submitBtn.disabled = false;
    submitBtn.textContent = 'Generate Video Pipeline';
    return;
  }

  setStatus('Sending request to pipeline...', 'info');

  try {
    const res = await postJSON('/api/jobs', payload);
    if (res.error) throw new Error(res.error);
    
    setStatus(`Job started successfully. ID: <b>${res.job_id}</b>. Connecting to stream...`, 'info');
    streamJob(res.job_id);
  } catch (e) {
    setStatus('Error: ' + e.message, 'error');
    submitBtn.disabled = false;
    submitBtn.textContent = 'Generate Video Pipeline';
  }
};

// Streaming Progress
function streamJob(jobId) {
  const evtSource = new EventSource('/api/jobs/' + jobId + '/stream');
  
  evtSource.onmessage = function(event) {
    const job = JSON.parse(event.data);
    let type = 'info';
    if (job.status === 'completed') type = 'success';
    if (job.status === 'failed') type = 'error';

    let progressHtml = '';
    if (job.status !== 'failed' && job.status !== 'completed') {
      progressHtml = `
        <div style="margin-top: 10px; background: rgba(255,255,255,0.1); height: 8px; border-radius: 4px; overflow: hidden;">
          <div style="width: ${job.progress_percentage || 5}%; background: var(--primary); height: 100%; transition: width 0.3s ease;"></div>
        </div>
        <div style="font-size: 0.85em; margin-top: 5px; color: var(--text-muted); display: flex; justify-content: space-between;">
          <span>${job.current_task || 'Processing...'}</span>
          ${job.current_model ? `<span>[${job.current_model}]</span>` : ''}
        </div>
      `;
    }

    setStatus(`
      <div style="font-weight: 600; margin-bottom: 8px;">Status: ${job.status.toUpperCase()}</div>
      <div>${job.message}</div>
      ${progressHtml}
    `, type);

    if (job.status === 'completed' || job.status === 'failed') {
      evtSource.close();
      submitBtn.disabled = false;
      submitBtn.textContent = 'Generate Video Pipeline';
      loadJobs('user-jobs-list');
    }
  };

  evtSource.onerror = function() {
    console.error("SSE connection error");
    evtSource.close();
  };
}

// Jobs Rendering
async function loadJobs(targetContainerId) {
  const container = document.getElementById(targetContainerId);
  if (!container) return;
  
  container.innerHTML = '<div style="color: var(--text-muted)">Loading jobs...</div>';
  try {
    const jobs = await getJSON('/api/jobs');
    if (!jobs.length) {
      container.innerHTML = '<div style="color: var(--text-muted)">No jobs found yet.</div>';
      return;
    }

    container.innerHTML = jobs.map(j => {
      const req = j.request || {};
      let badgeClass = 'badge-pending';
      if (j.status === 'completed') badgeClass = 'badge-completed';
      if (j.status === 'failed') badgeClass = 'badge-failed';

      let filesHtml = '';
      if (j.files) {
        filesHtml = '<ul class="file-links">';
        if (j.files.videos && j.files.videos.length) {
          filesHtml += `<li><a href="/api/download?path=${encodeURIComponent(j.files.videos[0])}" target="_blank">🎬 Download Final MP4</a></li>`;
        }
        if (j.files.script) {
          filesHtml += `<li><a href="/api/download?path=${encodeURIComponent(j.files.script)}" target="_blank">📄 View Script</a></li>`;
        }
        filesHtml += '</ul>';
      }

      let cancelBtnHtml = '';
      if (targetContainerId === 'admin-jobs-list' && !['completed', 'failed', 'cancelled'].includes(j.status)) {
        cancelBtnHtml = `<button onclick="cancelJob('${j.job_id}')" style="margin-top: 8px; background: var(--danger); color: white; padding: 4px 8px; border-radius: 4px; border: none; cursor: pointer; font-size: 0.8rem;">End Process</button>`;
      }

      return `
        <div class="job-card">
          <div class="job-header">
            <div class="job-topic">${req.topic || 'Batch Generation'}</div>
            <div class="job-badge ${badgeClass}">${j.status}</div>
          </div>
          <div class="job-meta">Mode: ${req.mode}</div>
          <div style="font-size: 0.9rem;">${j.message || ''}</div>
          ${filesHtml}
          ${cancelBtnHtml}
        </div>
      `;
    }).join('');
  } catch (e) {
    container.innerHTML = '<div style="color: var(--danger)">Failed to load jobs.</div>';
  }
}

document.getElementById('refresh-user-jobs').onclick = () => loadJobs('user-jobs-list');
document.getElementById('refresh-admin-jobs').onclick = () => loadJobs('admin-jobs-list');

window.cancelJob = async function(jobId) {
  if (!confirm('Are you sure you want to end this process permanently?')) return;
  try {
    await postJSON('/api/jobs/' + jobId + '/cancel', {});
    loadJobs('admin-jobs-list');
  } catch (e) {
    alert('Failed to end process: ' + e.message);
  }
};

// Admin Stats
async function loadAdminStats() {
  try {
    const health = await getJSON('/api/health');
    document.getElementById('health-api').textContent = health.ok ? 'ONLINE' : 'ERROR';
    document.getElementById('health-api').style.color = health.ok ? 'var(--success)' : 'var(--danger)';
    document.getElementById('health-planner').textContent = health.planner_model || 'N/A';
    document.getElementById('health-coding').textContent = health.coding_model || 'N/A';
    document.getElementById('health-utility').textContent = health.utility_model || 'N/A';
    document.getElementById('health-project').textContent = health.project;
  } catch (e) {
    document.getElementById('health-api').textContent = 'OFFLINE';
    document.getElementById('health-api').style.color = 'var(--danger)';
  }
}
