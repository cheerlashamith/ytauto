AUTOCOURSE FINAL MASTER PACKAGE - START HERE
=============================================

This is the FULLY AUTOMATIC version of AutoCourse Studio.

WHAT IS NEW IN THIS VERSION
---------------------------
✅ Fully automatic end-to-end video generation.
✅ Backend directly controls MoneyPrinterTurbo via its API (no manual upload).
✅ Backend directly controls Manim renderer (no manual copy/run).
✅ Backend directly controls ComfyUI story renderer (no manual copy/run).
✅ YouTube Extraction mode works: extracts transcript, rewrites script, generates video.
✅ Autonomous mode works: AI picks a topic, writes script, generates video via Pexels.
✅ Manual Course mode: syllabus-aware agent generates all subtopics, renders Manim clips, assembles final MP4.
✅ Story mode: AI writes story, ComfyUI generates images/clips, MPT assembles final MP4.
✅ Batch mode: leave topic empty to generate ALL 19 JNTUK R23 DSA topics automatically.
✅ Frontend shows progress only (planning -> rendering -> assembling -> done) and download button.
✅ No manual importing, no manual script pasting, no manual MPT usage.

HOW IT WORKS
------------
Frontend -> FastAPI Backend -> Ollama (script/plan) -> Renderer (Manim/ComfyUI/Pexels) -> MoneyPrinterTurbo API -> final MP4

PREREQUISITES
-------------
1. Python 3.10 or higher
2. Ollama installed and running with a model pulled (default: qwen2.5:7b)
3. MoneyPrinterTurbo portable installed at the path in config.json
4. FFmpeg installed and in PATH
5. Manim installed (for course mode)
6. ComfyUI installed and running (for story mode)
7. Pexels API key configured inside MoneyPrinterTurbo's config.toml (for autonomous/YouTube modes)

HOW TO RUN
----------
1. Start Ollama:
       ollama serve
   Make sure you have a model:
       ollama pull qwen2.5:7b

2. (For story mode) Start ComfyUI on http://127.0.0.1:8188

3. Extract this zip to C:\

4. Open CMD:
       cd /d C:\DOWNLOAD_ME_AutoCourse_Final_Master\01_main_app
       install.bat
       run.bat

5. Wait for: "Uvicorn running on http://127.0.0.1:8765"

6. Open browser to http://127.0.0.1:8765

7. Select a mode and click "Create Video".
   - Manual Course Mode: type a topic or leave empty for all 19 topics.
   - Story Mode: type a story topic.
   - YouTube Extraction Mode: paste a YouTube URL.
   - Autonomous Mode: leave topic empty for AI to pick a topic.

8. Wait for progress to reach "completed" and click "Download MP4".

IMPORTANT CONFIGURATION
-----------------------
Before running, edit this file:
    C:\DOWNLOAD_ME_AutoCourse_Final_Master\01_main_app\config.json

Set these paths correctly:
    "moneyprinter_root": "C:/MoneyPrinterTurbo-Portable-Windows-1.3.0/MoneyPrinterTurbo"
    "moneyprinter_api_url": "http://127.0.0.1:8080"
    "comfyui_url": "http://127.0.0.1:8188"
    "ollama_url": "http://127.0.0.1:11434"

Also set your Ollama model:
    "ollama_model": "qwen2.5:7b"

MONEYRPRINTERTURBO CONFIGURATION
--------------------------------
Open the MPT folder and copy config.example.toml to config.toml.
Edit config.toml and set:
    [app]
    pexels_api_keys = ["your-pexels-api-key-here"]

The first time you run AutoCourse, it will automatically start the MPT API server in the background.

STORY MODE WORKFLOW FILE
------------------------
Place your ComfyUI API workflow JSON at:
    C:\DOWNLOAD_ME_AutoCourse_Final_Master\01_main_app\engines\story_mode\workflows\sd3.5_simple_example_api.json

Export it from ComfyUI using "Save (API Format)" and rename it to sd3.5_simple_example_api.json.

OUTPUT FILES
------------
All generated files are in:
    C:\DOWNLOAD_ME_AutoCourse_Final_Master\01_main_app\outputs\<job_id>\

For batch mode, each topic has its own subfolder with:
    scenes_course.json
    moneyprinter_video_script.txt
    moneyprinter_keywords.txt
    final-1.mp4

TROUBLESHOOTING
---------------
- If Ollama is not running, the backend will show an error. Start it with "ollama serve".
- If MPT API is not running, the backend will try to start it automatically.
- If ComfyUI is not running, story mode will fail. Start it before using story mode.
- If Pexels API key is missing, autonomous/YouTube modes will fail. Add it to MPT config.toml.
- Check the full guide: AUTOCOURSE_MASTER_GUIDE.txt

NEXT STEPS
----------
Read AUTOCOURSE_MASTER_GUIDE.txt for the complete architecture, all modes, and professor presentation script.
