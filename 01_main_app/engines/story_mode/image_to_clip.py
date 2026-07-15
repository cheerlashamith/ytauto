import subprocess
from pathlib import Path

def image_to_clip(img,clip,duration=8,fps=30,ffmpeg='ffmpeg'):
    Path(clip).parent.mkdir(parents=True,exist_ok=True); frames=int(duration*fps)
    vf=("scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,"
        f"zoompan=z='min(1.0+0.06*on/{frames},1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={fps},format=yuv420p")
    subprocess.run([ffmpeg,'-y','-i',str(img),'-vf',vf,'-frames:v',str(frames),'-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(clip)],check=True)
