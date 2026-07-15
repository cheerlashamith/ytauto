# 🚀 Ubuntu Server Easy Setup Guide

Welcome to the Ubuntu Server! You don't need to type any of these long commands. Just use your mouse to highlight, copy, and paste them into the black Terminal window (press `Ctrl + Alt + T` to open it).

### Step 1: Download the Code to the Desktop
Copy and paste this into the terminal and hit Enter:
```bash
cd ~/Desktop && git clone https://github.com/cheerlashamith/ytauto.git && cd ytauto
```

### Step 2: Download the ComfyUI AI Models
Copy and paste this to grab your RealVisXL model straight from the internet:
```bash
mkdir -p comfyui_models && wget "https://huggingface.co/SG161222/RealVisXL_V5.0_Lightning/resolve/main/RealVisXL_V5.0_Lightning_fp16.safetensors" -O comfyui_models/realvisxlV50_v50LightningBakedvae.safetensors
```
*(Wait a few minutes for this to finish downloading!)*

### Step 3: Install the Magic Box (Docker)
We need to remove old conflicting versions first, then install the fresh ones. Copy and paste this:
```bash
sudo apt remove containerd -y && sudo apt update && sudo apt install docker.io docker-compose -y
```

### Step 4: Turn Everything On!
Copy and paste this to start the engines. It will take about 5-10 minutes to build the very first time.
```bash
sudo docker-compose up -d --build
```

### Step 5: Download the Text AI Brain
Copy and paste this to download the Qwen 2.5 brain for Ollama:
```bash
sudo docker exec -it autocourse-ollama ollama pull qwen2.5:7b
```

### Step 6: You are Done!
Open your browser and click on this link to view your website:
http://localhost:8765
