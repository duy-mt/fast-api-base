FROM python:alpine

WORKDIR /app

COPY requirements.txt . 

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python", "-m","uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload" ]