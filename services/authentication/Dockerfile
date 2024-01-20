FROM        python:3.11.7-bullseye

RUN         apt update -y && \
            apt upgrade -y

RUN         mkdir -p /microservice/authentication/

COPY        . /microservice/authentication/

RUN         pip install -r /microservice/authentication/requirements.txt

WORKDIR     /microservice/authentication/

CMD         [ "bash", "./tools/microservice-run.sh" ]