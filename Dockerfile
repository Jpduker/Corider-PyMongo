FROM python:3.9-alpine

WORKDIR /Corider-PyMongo

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD [ "python", "app.py" ]


