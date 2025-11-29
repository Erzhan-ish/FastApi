FROM python:3.12.8

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]

# docker build -t my_first_image .