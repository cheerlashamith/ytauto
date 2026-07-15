@echo off
cd /d %~dp0
python -m pip install -r requirements.txt
if not exist generated\clips mkdir generated\clips
python -m manim -ql render_stack_scenes.py StackScene01Intro -o scene_01_intro.mp4
python -m manim -ql render_stack_scenes.py StackScene02LIFO -o scene_02_lifo.mp4
python -m manim -ql render_stack_scenes.py StackScene03Push -o scene_03_push.mp4
python -m manim -ql render_stack_scenes.py StackScene04Pop -o scene_04_pop.mp4
python -m manim -ql render_stack_scenes.py StackScene05Peek -o scene_05_peek.mp4
python -m manim -ql render_stack_scenes.py StackScene06Uses -o scene_06_uses.mp4
python -m manim -ql render_stack_scenes.py StackScene07Summary -o scene_07_summary.mp4
for /R media\videos\render_stack_scenes %%f in (*.mp4) do copy /Y "%%f" generated\clips\ >nul
echo.
echo DONE rendering scenes. Clips copied to generated\clips
dir generated\clips\*.mp4
pause
