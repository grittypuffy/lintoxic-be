FROM python:3.12-slim-bookworm

ENV VIRTUAL_ENV=lintoxic-api

RUN apt-get update
RUN apt-get install -y \
    libgl1 \
    libglib2.0-0

RUN apt-get install -y clang \
    pkg-config \
    libcairo2-dev \ 
    cmake \
    gobject-introspection \
    libgirepository1.0-dev

RUN rm -rf /var/lib/apt/lists/*

RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="/$VIRTUAL_ENV/bin:$PATH"

WORKDIR /lintoxic-api

COPY requirements.txt .

COPY README.md .

COPY pyproject.toml .

COPY .env .

COPY ./api ./api

RUN . ./bin/activate && pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    libgdk-pixbuf2.0 \
    libgdk-pixbuf-2.0-dev \
    gir1.2-gdkpixbuf-2.0 \
    libglib2.0-dev \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    librsvg2-2 \
    gir1.2-rsvg-2.0 \
    librsvg2-dev

RUN apt-get update && apt-get upgrade && apt-get install -y \
    poppler-utils \
    libpoppler-glib-dev \
    libgirepository1.0-dev 

ENTRYPOINT ["fastapi", "dev", "api/server.py"]