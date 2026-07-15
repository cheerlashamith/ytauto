import json, pathlib

outputs = pathlib.Path('outputs')
for job_dir in outputs.iterdir():
    job_file = job_dir / 'job.json'
    if not job_file.exists():
        continue
    data = json.loads(job_file.read_text(encoding='utf-8'))
    files = data.get('files', {})
    if 'final_video' not in files and files.get('videos'):
        files['final_video'] = files['videos'][0]
        data['files'] = files
        job_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        print('Patched', job_dir.name)
    else:
        print('Skipped', job_dir.name)
