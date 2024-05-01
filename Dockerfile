FROM eclipse-temurin:22.0.1_8-jdk-alpine

WORKDIR /app

RUN apk add --no-cache \
    bash curl \
    py3-pip \
    libreoffice \
    supervisor

# fonts - https://wiki.alpinelinux.org/wiki/Fonts
RUN apk add --no-cache \
    font-noto font-noto-cjk font-noto-extra \
    terminus-font \
    ttf-font-awesome \
    ttf-dejavu \
    ttf-freefont \
    ttf-hack \
    ttf-inconsolata \
    ttf-liberation \
    ttf-mononoki  \
    ttf-opensans   \
    fontconfig && \
    fc-cache -f

RUN rm -rf /var/cache/apk/* /tmp/*

COPY ./pyproject.toml .
COPY ./src/ ./src

RUN pip install --break-system-packages -e .

RUN addgroup -S unoserver && adduser -S unoserver -G unoserver
USER unoserver

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app/src/"

CMD ["python", "src/unoserver/server.py", "--protocol=grpc", "--port=50051"]

EXPOSE 50051
