# syntax = docker/dockerfile:1.0.2-experimental

#####################
### builder image ###
FROM python:3.8.5-slim-buster as builder

RUN useradd --create-home --shell /bin/bash app

COPY --chown=app:app ./requirements.txt /home/app/requirements.txt
ENV BUILD_REQS='build-essential gcc ca-certificates gnupg'
ENV RUNTIME_REQS='git gettext'
ENV EXTRA_PACKAGES='curl netcat vim'

RUN apt update -y -qq && \
    apt install -y --no-install-recommends $BUILD_REQS $EXTRA_PACKAGES && \
    apt update -y -qq && \
    apt install -y --no-install-recommends $RUNTIME_REQS && \
    pip install -r /home/app/requirements.txt && \
    apt purge -y $BUILD_REQS && \
    apt autoremove -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

COPY --chown=app:app ./ /home/app/
RUN pip install --no-cache-dir -e /home/app/

WORKDIR /home/app

ARG USER_ID
ARG GROUP_ID

RUN usermod -u ${USER_ID} app && \
    groupmod -g ${GROUP_ID} app

RUN mkdir /static && chown -R app:app /static
RUN chown -R app:app /home/app

RUN mkdir /sqlite3 && chown -R app:app /sqlite3
RUN chown -R app:app /sqlite3

USER app

########################
### production image ###
FROM builder as production

# For gunicorn configuration check https://pythonspeed.com/articles/gunicorn-in-docker/
# Configuration
# - use memory for worker hardbeat
# - 2 workers
# - 4 threads
# - log to stdout
CMD ["gunicorn", \
     "--worker-tmp-dir", "/dev/shm", \
     "--workers", "2", \
     "--threads", "4", \
     "--worker-class", "gthread", \
     "--log-file", "-", \
     "gt.wsgi", \
     "--keep-alive", "75", \
     "-b", "0.0.0.0:8000"]

#########################
### development image ###
FROM builder as development

COPY --chown=app:app docker/wait-for.sh /wait-for.sh

# Configured to reload gt on code change
CMD ["gunicorn", \
     "--reload", \
     "--log-file", "-", \
     "--timeout", "0", \
     "gt.wsgi", \
     "-b", "0.0.0.0:8000"]

