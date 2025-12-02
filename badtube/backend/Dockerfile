FROM python:3.13-alpine

WORKDIR /app

# for production
# COPY code .

COPY requirements.txt ./requirements.txt
RUN apk add --no-cache ffmpeg
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["fastapi", "dev", "code/app.py", "--host", "0.0.0.0"]
