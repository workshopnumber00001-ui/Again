# Base image update kiya gaya (Bullseye -> Bookworm)
FROM python:3.12.3-slim-bookworm

# System dependencies install karo
RUN apt-get update && apt-get install -y --no-install-recommends --fix-missing \
    build-essential \
    gcc \
    musl-dev \
    libffi-dev \
    libssl-dev \
    libglib2.0-0 \
    libmagic1 \
    libexif6 \
    libxrender-dev \
    libsm6 \
    ca-certificates \
    wget \
    aria2 \
    curl \
    unzip \
    mkvtoolnix \
    mkvtoolnix-gui \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Install latest FFmpeg (includes ffprobe)
RUN wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    && tar -xf ffmpeg-release-amd64-static.tar.xz \
    && mv ffmpeg-*/ffmpeg /usr/local/bin/ \
    && mv ffmpeg-*/ffprobe /usr/local/bin/ \
    && rm -rf ffmpeg-*

# Install N_m3u8DL-RE
RUN wget https://github.com/nilaoda/N_m3u8DL-RE/releases/download/v0.2.0-beta/N_m3u8DL-RE_Beta_linux-x64_20230628.tar.gz \
    && tar -xzf N_m3u8DL-RE_Beta_linux-x64_20230628.tar.gz -C /opt/ \
    && mv /opt/N_m3u8DL-RE_Beta_linux-x64/N_m3u8DL-RE /usr/local/bin/ \
    && chmod +x /usr/local/bin/N_m3u8DL-RE \
    && rm -rf N_m3u8DL-RE_Beta_linux-x64_20230628.tar.gz \
    && rm -rf /opt/N_m3u8DL-RE_Beta_linux-x64

# Install Bento4 (for mp4decrypt)
RUN wget https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip \
    && unzip Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip -d /opt/bento4 \
    && mv /opt/bento4/Bento4-SDK-1-6-0-641.x86_64-unknown-linux/bin/mp4decrypt /usr/local/bin/ \
    && chmod +x /usr/local/bin/mp4decrypt \
    && rm Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip \
    && rm -rf /opt/bento4

# Copy files and set workdir
COPY . /app
WORKDIR /app

# Install Python requirements
RUN pip install --no-cache-dir --upgrade --requirement requirements.txt

# Run the bot
CMD ["python3", "Modules/main.py"]
