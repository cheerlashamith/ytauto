import argparse,json,os,tomli as tomllib
from pathlib import Path
from comfyui_client import ComfyUIClient,load_workflow
from image_to_clip import image_to_clip

def loadcfg():
    p='config.toml' if os.path.exists('config.toml') else 'config.example.toml'
    return tomllib.load(open(p,'rb'))
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--scenes',default='scenes_story.json'); a=ap.parse_args(); c=loadcfg(); data=json.load(open(a.scenes,encoding='utf-8'))
    out=Path(c.get('output_dir','generated')); img=out/'images'; clips=out/'clips'; img.mkdir(parents=True,exist_ok=True); clips.mkdir(parents=True,exist_ok=True)
    wf=load_workflow(c['workflow_path']); client=ComfyUIClient(c.get('comfyui_url','http://127.0.0.1:8188')); print('Checking ComfyUI...'); client.health(); paths=[]
    for i,s in enumerate(data['scenes'],1):
        name=s.get('name',f'scene_{i:02d}'); raw=img/f'{name}.png'; clip=clips/f'{name}.mp4'; print(f'[{i}/{len(data["scenes"])}] {name}')
        client.generate_image(wf,s['prompt'],c.get('negative_prompt',''),raw,c.get('width',1080),c.get('height',1920),c.get('steps',20),c.get('cfg',4.0)); print('Story Mode: no overlay')
        image_to_clip(raw,clip,c.get('clip_duration',8),c.get('fps',30),c.get('ffmpeg','ffmpeg')); paths.append(str(clip.resolve()))
    (out/'moneyprinter_local_materials.txt').write_text(','.join(paths),encoding='utf-8'); (out/'moneyprinter_video_script.txt').write_text(data.get('moneyprinter_script',''),encoding='utf-8'); (out/'moneyprinter_keywords.txt').write_text(data.get('keywords',''),encoding='utf-8'); print('DONE')
