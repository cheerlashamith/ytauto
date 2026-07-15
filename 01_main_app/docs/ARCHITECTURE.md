# AutoCourse Studio Final Project Architecture

## Modes

1. Manual Course Mode
2. Story Mode
3. YouTube Extraction Mode
4. Autonomous Mode

## Flow

```text
Frontend -> FastAPI Backend -> Scene Planner -> Visual Router -> External Renderers -> MoneyPrinterTurbo -> Final MP4
```

## Current Implementation

The backend currently generates structured plans, scripts, and keywords in `outputs/JOB_ID`.
Rendering is still performed through the existing external engines:

- ComfyUI Story Mode folder
- Manim Course Mode folder
- MoneyPrinterTurbo Local File mode

## Why This Project Exists

MoneyPrinterTurbo is a strong render engine, but the product needs a custom frontend and backend that can manage multiple modes.

## Visual Modes

- Story: ComfyUI
- Course: Manim
- Autonomous/general: Pexels/ComfyUI/Manim depending topic
- YouTube extraction: chosen by extracted content

## Next Step

Replace manual external rendering with native subprocess adapters and then direct integration.
