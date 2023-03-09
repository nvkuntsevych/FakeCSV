FROM python:3.11

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN apt update
RUN apt install -y netcat

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN sed -i 's/\r$//g' /usr/src/scripts/start.sh
RUN chmod +x /usr/src/scripts/start.sh

ENTRYPOINT ["/usr/src/scripts/start.sh"]
