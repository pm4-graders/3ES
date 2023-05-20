FROM python:3.9

COPY ./requirements.txt /code/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

COPY . /code/app

WORKDIR /code/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]