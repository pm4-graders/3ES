FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# install stuff for cv2
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

#EXPOSE 5000

#USER app
