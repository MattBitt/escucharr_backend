# # For more information, please refer to https://aka.ms/vscode-docker-python
# FROM python:3.10


# # Keeps Python from generating .pyc files in the container
# ENV PYTHONDONTWRITEBYTECODE=1

# # Turns off buffering for easier container logging
# ENV PYTHONUNBUFFERED=1

# #install ffmpeg
# RUN apt-get update -qq && apt-get -y install ffmpeg

# RUN pip install --upgrade pip

# RUN pip install yt-dlp


# # Install pip requirements
# COPY src/requirements.txt .
# RUN pip install -r requirements.txt

# WORKDIR /app
# COPY . /app

# # Creates a non-root user with an explicit UID and adds permission to access the /app folder
# # For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# #RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# #USER appuser

# # During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["python", "-m", "app"]




# pull official base image
FROM python:3.10.0-alpine

# set work directory
WORKDIR /usr/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /usr/app/requirements.txt

# install dependencies

RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
    openssl-dev libffi-dev gcc musl-dev python3-dev \
    postgresql-dev bash git ffmpeg\
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/app/requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY . /usr/app/

CMD ["python", "-m", "main"]