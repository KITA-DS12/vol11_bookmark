FROM python:3.8-slim

WORKDIR /server


COPY ./src/server/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /server/requirements.txt

COPY ./src/server .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8888"]
