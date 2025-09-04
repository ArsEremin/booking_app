FROM python:3.12

RUN mkdir /booking_app

WORKDIR /booking_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

CMD ["/booking_app/docker/app.sh"]
