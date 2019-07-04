FROM python:3.6

EXPOSE 5000

WORKDIR /app

COPY requirements.txt .

COPY app.py .

COPY base.py .

RUN pip3 install -r requirements.txt

CMD python app.py
