FROM python:3.10

RUN mkdir -p /opt
WORKDIR /opt

COPY . /opt/

RUN pip install pip
RUN pip install pipenv
RUN pipenv install

ENTRYPOINT [ "pipenv", "run", "python3", "main.py" ]