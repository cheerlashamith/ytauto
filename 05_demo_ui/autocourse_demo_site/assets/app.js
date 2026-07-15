function runDemo(){
  document.querySelectorAll('.step').forEach((s,i)=>{
    const state=s.querySelector('.state');
    if(state) state.textContent='Queued';
    s.style.borderColor='rgba(222,219,200,.14)';
    setTimeout(()=>{ if(state) state.textContent=['Planning','Generating','Overlaying','Rendering'][i]||'Done'; s.style.borderColor=i===3?'rgba(114,237,167,.55)':'rgba(169,139,255,.55)';},500+i*650);
  });
}
function addLog(){
  const box=document.getElementById('logBox'); if(!box)return;
  const msgs=['<span class="green">[OK]</span> final-1.mp4 exported','<span class="violet">[COMFY]</span> scene background generated','<span class="green">[OVERLAY]</span> clean text rendered','<span class="yellow">[FFMPEG]</span> combining clips','<span class="violet">[OLLAMA]</span> scene plan completed'];
  const d=document.createElement('div');d.className='log-line';d.innerHTML=msgs[Math.floor(Math.random()*msgs.length)];box.appendChild(d);box.scrollTop=box.scrollHeight;
}
setInterval(addLog,5000);
