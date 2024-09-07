FROM python

RUN apt update

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

RUN pip3 install gunicorn

EXPOSE 5000

CMD gunicorn -w 4 -b 0.0.0.0:5000 app:app