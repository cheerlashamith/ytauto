# Setup and Run

## 1. Extract

Extract zip to:

```text
C:\AutoCourse_Studio_Final_Project
```

## 2. Install backend

```cmd
cd /d C:\AutoCourse_Studio_Final_Project
install.bat
```

## 3. Run backend/frontend

```cmd
run.bat
```

Open:

```text
http://127.0.0.1:8765
```

## 4. Create a plan

Use the frontend Generate page.

## 5. Output

Generated plan files are in:

```text
outputs\JOB_ID
```

## 6. Render

For course mode:
- copy scenes_course.json into Manim renderer folder
- render clips
- upload clips to MoneyPrinterTurbo

For story mode:
- copy scenes_story.json into ComfyUI story mode folder
- generate clips
- upload clips to MoneyPrinterTurbo
