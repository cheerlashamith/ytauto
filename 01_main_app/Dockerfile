# Stage 1: Build the React frontend v2
FROM node:18 AS frontend-builder
WORKDIR /app/frontend_v2
COPY frontend_v2/package*.json ./
RUN npm install
COPY frontend_v2/ ./
RUN npm run build

# Stage 2: Python Backend
FROM python:3.10-slim

# Install system dependencies for Manim and FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libcairo2-dev \
    libpango1.0-dev \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-latex-recommended \
    texlive-science \
    tipa \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python requirements first to leverage Docker cache
COPY backend/requirements.txt ./backend/
COPY engines/story_mode/requirements.txt ./engines/story_mode/
COPY engines/manim_course_mode/requirements.txt ./engines/manim_course_mode/

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt
RUN pip install --no-cache-dir -r engines/story_mode/requirements.txt
RUN pip install --no-cache-dir -r engines/manim_course_mode/requirements.txt

# Copy backend application code
COPY . .

# Copy the built v2 frontend from Stage 1
COPY --from=frontend-builder /app/frontend_v2/dist ./frontend_v2/dist

# Expose backend API port
EXPOSE 8765

CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8765"]
