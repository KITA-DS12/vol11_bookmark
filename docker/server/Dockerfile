FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

WORKDIR /server

RUN apt-get update && apt-get install python3.8 python3-pip -y
COPY ./src/server/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /server/requirements.txt

COPY ./src/server .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8888"]
