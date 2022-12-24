FROM python:latest

ADD chats_handler.py /bot/
ADD main.py /bot/
ADD paths.py /bot/
ADD tg_exceptions.py /bot/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

WORKDIR /bot/