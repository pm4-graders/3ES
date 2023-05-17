FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY --from=continuumio/miniconda3:4.12.0 /opt/conda /opt/conda

ENV PATH=/opt/conda/bin:$PATH

# install stuff for cv2
RUN set -ex && \
    conda config --set always_yes yes --set changeps1 no && \
    conda info -a && \
    conda config --add channels conda-forge && \
    conda install --quiet --freeze-installed -c main conda-pack

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

#EXPOSE 5000

#USER app
