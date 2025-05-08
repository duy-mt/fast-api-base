FROM python:alpine

WORKDIR /app

COPY requirements.txt . 

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "-m","uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]