FROM python:3.7.5-slim

RUN useradd -m -s /bin/bash -d /home/jenkins jenkins

WORKDIR /home/jenkins/uber

COPY ./requirements.txt /home/jenkins/uber

RUN python -m pip install -r /home/jenkins/uber/requirements.txt

COPY . /home/jenkins/uber

RUN chown -R jenkins:jenkins /home/jenkins/uber/ && chmod -R 775 /home/jenkins/uber/ && \
    mkdir -p /var/log/uber && chown  -R jenkins:jenkins /var/log/uber

RUN mkdir /home/jenkins/uber/staticfiles/
RUN chown -R jenkins:jenkins /home/jenkins/uber/staticfiles/