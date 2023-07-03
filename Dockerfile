FROM python:3.11-bullseye

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app
COPY ./start /start
RUN chmod +x /start

CMD ["/start"]