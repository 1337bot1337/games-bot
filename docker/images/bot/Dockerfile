FROM python:3.8.2

RUN mkdir /src

COPY ./bot /src/bot/

WORKDIR /src/bot

RUN pip install -r requirements.txt

EXPOSE 8081

CMD ["python", "-u", "run.py"]