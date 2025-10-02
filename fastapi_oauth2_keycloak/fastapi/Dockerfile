FROM python:3.13-slim-bookworm

WORKDIR /app

COPY ./src .
COPY ./requirements.txt libs.txt

RUN python -m pip install --upgrade pip 
RUN pip install --no-cache -r libs.txt

CMD ["fastapi", "dev", "app.py", "--port", "8080", "--host", "0.0.0.0"]