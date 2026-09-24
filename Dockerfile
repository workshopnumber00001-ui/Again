FROM python:3.12.3-slim-bullseye
#3.10.13-slim


RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        build-essential gcc musl-dev libffi-dev libssl-dev \
        libglib2.0-0 libmagic1 libxext6 libxrender-dev libsm6 \
        ca-certificates wget git aria2 curl unzip mkvtoolnix mkvtoolnix-gui wkhtmltopdf  \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install latest FFmpeg (includes ffprobe)
RUN wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    && tar -xJf ffmpeg-release-amd64-static.tar.xz \
    && mv ffmpeg-*/ffmpeg /usr/local/bin/ \
    && mv ffmpeg-*/ffprobe /usr/local/bin/ \
    && rm -rf ffmpeg-*

RUN wget https://github.com/nilaoda/N_m3u8DL-RE/releases/download/v0.2.0-beta/N_m3u8DL-RE_Beta_linux-x64_20230628.tar.gz \
    && tar -xzf N_m3u8DL-RE_Beta_linux-x64_20230628.tar.gz -C /opt/ \
    && mv /opt/N_m3u8DL-RE_Beta_linux-x64/N_m3u8DL-RE /usr/local/bin/ \
    && chmod +x /usr/local/bin/N_m3u8DL-RE \
    && rm N_m3u8DL-RE_Beta_linux-x64_20230628.tar.gz \
    && rm -rf /opt/N_m3u8DL-RE_Beta_linux-x64

RUN wget https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip \
    && unzip Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip -d /opt/bento4 \
    && mv /opt/bento4/Bento4-SDK-1-6-0-641.x86_64-unknown-linux/bin/mp4decrypt /usr/local/bin/ \
    && chmod +x /usr/local/bin/mp4decrypt \
    && rm Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip \
    && rm -rf /opt/bento4

COPY . /app/
WORKDIR /app/

RUN pip install --no-cache-dir --upgrade --requirement requirements.txt


CMD ["python3", "Modules/main.py"]
