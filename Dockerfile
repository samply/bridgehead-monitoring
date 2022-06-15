FROM python:3-slim


WORKDIR /usr/src/app

RUN pip install requests

# See exact list of files in .dockerignore
ADD src/ /usr/src/app/

CMD ["python", "-u", "app.py"]