# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set Work Directory
WORKDIR /app

# Install pip requirements
COPY requirements.txt requirements.txt
# RUN python3 -m pip install -r requirements.txt
RUN pip3 install -r requirements.txt   

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
