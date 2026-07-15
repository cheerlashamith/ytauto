import json, os, shutil, subprocess, sys
from pathlib import Path
data=json.load(open('scenes_course.json',encoding='utf-8'))
clips=Path('generated/clips'); clips.mkdir(parents=True,exist_ok=True)
for f in clips.glob('*.mp4'): f.unlink()
for i,sc in enumerate(data.get('scenes',[])):
    name=sc.get('name',f'scene_{i:02d}')+'.mp4'; env=os.environ.copy(); env['SCENE_INDEX']=str(i)
    print('Rendering',name)
    subprocess.run([sys.executable,'-m','manim','-ql','render_course.py','UltimateCourseScene','-o',name],check=True,env=env)
    found=list(Path('media').rglob(name))
    if found: shutil.copy2(found[-1],clips/name)
mp=data.get('moneyprinter_script','')
if isinstance(mp,dict): mp=mp.get('full_voiceover') or '\n\n'.join(mp.get('paragraphs',[]))
kw=data.get('keywords','')
if isinstance(kw,list): kw=', '.join(kw)
Path('generated/moneyprinter_video_script.txt').write_text(str(mp),encoding='utf-8')
Path('generated/moneyprinter_keywords.txt').write_text(str(kw),encoding='utf-8')
print('DONE clips:',clips.resolve())
