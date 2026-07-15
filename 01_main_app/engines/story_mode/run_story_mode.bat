@echo off
cd /d %~dp0
set /p TOPIC=Enter kids story topic: 
python -m pip install -r requirements.txt
python generate_story_scenes.py --topic "%TOPIC%" --out scenes_story.json
echo Edit scenes_story.json now if needed. Press any key to create story clips.
pause
python generate_story_materials.py --scenes scenes_story.json
pause
