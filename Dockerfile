FROM python:3-slim

WORKDIR /usr/src/app

# See exact list of files in .dockerignore
ADD src/ /usr/src/app/